#!/usr/bin/env python3
"""run — Deep Agent Process runner for the Systems Thinking Studio.

Bounded multi-pass deep-research/deep-work loop over one question:

  QUESTION -> DECOMPOSE -> PARALLEL GATHER (passes) -> ADVERSARIAL VERIFY
  -> SYNTHESIZE -> SEAL

Deterministic-first (A1): every corpus/data touch is the `studio` CLI or a
local grep of `knowledge/`; LLM passes (local proxy, OpenAI-compatible) only
reason over deterministic output; every phase has a deterministic check; the
run seals via the studio's `proofpacket/seal.py` + `verify.py`. Process
contract: `processes/deep-agent/procedure.md`. Trace sidecar:
`processes/deep-agent/trace-schema.md` (LangSmith-compatible JSONL).

Usage:
  python3 scripts/deep_agent/run.py "<question>" [options]

Options:
  --dry-run          full plumbing, zero LLM calls; artifacts marked DRY-RUN
  --max-passes N     gather passes (default 3)
  --verify N         adversarial votes per claim (default 2)
  --model M          proxy model for gather/verify (default claude-haiku-4-5)
  --reason-model M   model for question/decompose/synthesize (default claude-sonnet-4-5)
  --max-claims N     claims taken into adversarial verify (default 8)
  --recall           enable optional web layer: `studio search` (Recall KB)
  --timeout S        per-LLM-call timeout (default 240)
  --runs-root DIR    run parent dir (default ~/.rig/systems-studio/runs/deep-agent)
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

STUDIO = Path(__file__).resolve().parents[2]
PROXY_BASE = "http://127.0.0.1:8317/v1"
KEY_NAME = "KIMI_SUB_API_KEY"  # local fleet proxy key in ~/.hermes/.env (never printed)
RUN_TYPE_ROOT = "deep-agent-run"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trace import TraceWriter  # noqa: E402  (sibling module, stdlib only)

STOPWORDS = set("""the and for that this with from have has are was were will would could
should what when where which whom whose into onto over under about after before between
their there these those they them then than some such only also just very much many more
most less least our your its it's you've we're don't doesn't isn't been being because
does doing done each few same still such take takes taking make makes making get gets
getting give gives giving how why who whom while during through against above below off
once here all any both each no nor not own so too can may might must shall""".split())


# ---------------------------------------------------------------- helpers
def load_key() -> str:
    """KIMI_SUB_API_KEY from env, then ~/.hermes/.env. Never echoed."""
    import os
    k = os.environ.get(KEY_NAME, "")
    if k:
        return k
    p = Path.home() / ".hermes" / ".env"
    if p.is_file():
        for line in p.read_text().splitlines():
            if line.startswith(KEY_NAME + "="):
                return line.split("=", 1)[1].strip()
    return ""


class LLMError(Exception):
    pass


def llm(messages: list[dict], model: str, timeout: int, max_tokens: int = 1200,
        retries: int = 2) -> tuple[str, dict]:
    """One chat completion against the local proxy. No temperature (proxy rejects != 1)."""
    key = load_key()
    if not key:
        raise LLMError(f"no {KEY_NAME} (env or ~/.hermes/.env)")
    body = json.dumps({"model": model, "messages": messages,
                       "max_tokens": max_tokens}).encode()
    last = ""
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            PROXY_BASE + "/chat/completions", data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.load(r)
            text = (d.get("choices") or [{}])[0].get("message", {}).get("content", "")
            usage = d.get("usage") or {}
            usage["wall_seconds"] = round(time.time() - t0, 1)
            if not text.strip():
                raise LLMError("empty completion")
            return text, usage
        except Exception as exc:  # noqa: BLE001 — network/HTTP/parse alike
            last = f"{type(exc).__name__}: {exc}"
            if attempt < retries:
                time.sleep(4 * (attempt + 1))
    raise LLMError(last)


def extract_json(text: str) -> dict:
    """Tolerant JSON extraction: fenced block, else first '{' to last '}'."""
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    raw = m.group(1) if m else (text[text.find("{"):text.rfind("}") + 1]
                                if "{" in text and "}" in text else "")
    if not raw:
        raise LLMError("no JSON object found in model output")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LLMError(f"malformed/truncated JSON from model ({exc.msg} at "
                       f"pos {exc.pos}; likely max_tokens cutoff): ...{raw[-60:]!r}") from exc


def keywords(text: str, n: int = 6) -> list[str]:
    """Deterministic keyword extraction for corpus greps."""
    words = re.findall(r"[a-zA-Z][a-zA-Z'-]{3,}", text.lower())
    freq: dict[str, int] = {}
    for w in words:
        if w in STOPWORDS:
            continue
        freq[w] = freq.get(w, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:n]]


def run_cmd(argv: list[str], timeout: int = 60, cwd: Path | None = None) -> tuple[int, str]:
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        return p.returncode, (p.stdout or "") + (("\n[stderr] " + p.stderr) if p.stderr.strip() else "")
    except subprocess.TimeoutExpired:
        return 124, "(timeout)"
    except FileNotFoundError:
        return 127, "(command not found)"


# ---------------------------------------------------------------- gatherers
def gather_studio(sq: str) -> str:
    rc, out = run_cmd([sys.executable, str(STUDIO / "scripts/studio.py"), "map", sq])
    return f"$ studio map <sub-question>\n(exit {rc})\n{out.strip()[:2200]}"


def gather_cards(kw: str) -> str:
    rc, out = run_cmd([sys.executable, str(STUDIO / "scripts/studio.py"),
                       "cards", "systems-thinking", "--grep", kw])
    return f"$ studio cards systems-thinking --grep {kw}\n(exit {rc})\n{out.strip()[:1800]}"


def gather_knowledge(kws: list[str]) -> str:
    """Deterministic grep over the distilled knowledge library (titles + bodies)."""
    chunks = []
    root = STUDIO / "knowledge"
    for sub in ("youtube", "papers", "books"):
        d = root / sub
        if not d.is_dir():
            continue
        files = sorted(d.glob("*.md"))
        hits = []
        for f in files:
            try:
                body = f.read_text(errors="replace").lower()
            except OSError:
                continue
            score = sum(body.count(k) for k in kws if len(k) > 4)
            if score >= 2:
                hits.append((score, f))
        for score, f in sorted(hits, key=lambda x: -x[0])[:6]:
            first = f.read_text(errors="replace").splitlines()
            head = next((l.strip("# ") for l in first if l.strip().startswith("#")), f.name)
            chunks.append(f"- [{sub}/{f.name}] (score {score}) {head[:120]}")
    return ("$ grep knowledge/{youtube,papers,books} keywords=" + ",".join(kws)
            + f"\n({len(chunks)} source hits)\n" + "\n".join(chunks))


def gather_recall(query: str) -> str:
    """Optional web layer (Recall KB). Fail-soft: unavailable is a finding, not a crash."""
    rc, out = run_cmd([sys.executable, str(STUDIO / "scripts/studio.py"),
                       "search", query, "focused"], timeout=75)
    return f"$ studio search <query> focused  (optional web layer)\n(exit {rc})\n{out.strip()[:2400]}"


# ---------------------------------------------------------------- phases
def phase_question(run: Path, trace: TraceWriter, q: str, model: str,
                   timeout: int, dry: bool) -> tuple[str, bool]:
    art = run / "question.md"
    with trace.phase("D0-question", inputs={"question": q}):
        err = None
        body = ""
        if dry:
            body = (f"# Deep-agent run — question (DRY-RUN, no LLM)\n\n"
                    f"## Restated question\n\n{q} (restated verbatim: dry-run)\n\n"
                    f"## Success looks like\n\n- DRY-RUN: plumbing check only\n\n"
                    f"## Symptom vocabulary\n\n- (dry-run: none extracted)\n\n"
                    f"## Unknowns\n\n- DRY-RUN: all LLM passes skipped\n")
        else:
            prompt = [
                {"role": "system", "content": "You restate research questions precisely. Be terse."},
                {"role": "user", "content":
                 f"Restate this question for a bounded deep-research run:\n---\n{q}\n---\n"
                 "Write markdown with EXACTLY these sections:\n"
                 "## Restated question\n## Success looks like\n(3-4 observable outcomes)"
                 "\n## Symptom vocabulary\n(plain verbs+nouns from the question: plateau, "
                 "stall, keeps coming back, quick fix...)\n## Unknowns\n(what is NOT given; "
                 "write Unknown where absent — never invent numbers)"}]
            try:
                t0 = time.time()
                body, usage = llm(prompt, model, timeout, max_tokens=700)
                trace.llm_call("question-restatement", model, prompt, body, usage,
                               start_time=None, tags=["phase:question"])
            except Exception as exc:  # noqa: BLE001 — degrade honestly
                err = str(exc)
                trace.llm_call("question-restatement", model, prompt, "", error=err,
                               tags=["phase:question", "failed"])
                body = (f"# Deep-agent run — question (DEGRADED: LLM unavailable)\n\n"
                        f"## Restated question\n\n{q}\n\n## Success looks like\n\n"
                        "- needs-agent-reasoning (LLM pass failed)\n\n"
                        f"## Symptom vocabulary\n\n- (llm error: {err})\n\n## Unknowns\n\n- all\n")
        art.write_text(body)
        ok = bool(re.search(r"(?im)^## Restated question", body)) and \
            bool(re.search(r"(?im)^## Success looks like", body))
        trace.set_outputs({"artifact": art.name, "check": "PASS" if ok else "FAIL",
                           "error": err})
    return str(art), ok


def phase_decompose(run: Path, trace: TraceWriter, q: str, question_md: str,
                    model: str, timeout: int, dry: bool) -> tuple[list[str], bool]:
    art_md, art_js = run / "decompose.md", run / "decompose.json"
    with trace.phase("D1-decompose", inputs={"question": q}):
        subs: list[str] = []
        err = None
        if dry:
            sents = [s.strip() for s in re.split(r"(?<=[.?])\s+", q) if len(s.strip()) > 12]
            subs = sents[:5] or [q]
            source = "deterministic sentence split (dry-run)"
        else:
            prompt = [
                {"role": "system", "content": "You decompose research questions. JSON only."},
                {"role": "user", "content":
                 f"Question: {q}\n\nRestated brief:\n{question_md[:1500]}\n\n"
                 "Decompose into 3-6 independently answerable sub-questions. "
                 'Return ONLY JSON: {"subquestions": ["...", ...]}'}]
            try:
                t, usage = llm(prompt, model, timeout, max_tokens=500)
                trace.llm_call("decompose", model, prompt, t, usage, tags=["phase:decompose"])
                subs = [s.strip() for s in extract_json(t).get("subquestions", []) if s.strip()]
                if not (3 <= len(subs) <= 6):
                    raise LLMError(f"subquestion count {len(subs)} outside 3..6")
                source = "LLM decomposition"
            except Exception as exc:  # noqa: BLE001 — degrade honestly
                err = str(exc)
                trace.llm_call("decompose", model, prompt, "", error=err,
                               tags=["phase:decompose", "failed"])
                sents = [s.strip() for s in re.split(r"(?<=[.?])\s+", q) if len(s.strip()) > 12]
                subs = sents[:5] or [q]
                source = f"DEGRADED fallback sentence split (llm error: {err[:120] if isinstance(err, str) else err})"
        art_js.write_text(json.dumps({"subquestions": subs, "source": source,
                                      "error": err}, indent=2) + "\n")
        lines = [f"# Deep-agent decomposition", "",
                 f"Source: {source}", "", "## Sub-questions", ""]
        lines += [f"{i}. {s}" for i, s in enumerate(subs, 1)]
        lines += ["", "## Coverage check", "",
                  "- each sub-question is independently evidence-gatherable (map/cards/"
                  "knowledge greps apply per sub-question)", ""]
        art_md.write_text("\n".join(lines))
        ok = len(subs) >= 1 and "## Sub-questions" in "\n".join(lines)
        trace.set_outputs({"subquestions": len(subs), "check": "PASS" if ok else "FAIL"})
    return subs, ok


def gather_pass(run: Path, trace: TraceWriter, subs: list[str], pass_no: int,
                model: str, timeout: int, dry: bool, use_recall: bool,
                followups: dict[int, str] | None = None) -> list[dict]:
    """One gather pass: deterministic corpus pulls + (parallel) LLM extraction."""
    findings: list[dict] = []
    with trace.phase(f"D2-gather-pass{pass_no}",
                     inputs={"subquestions": len(subs), "dry_run": dry}):
        evidence_files: list[tuple[int, str, Path]] = []

        def det_gather(i_sq: tuple[int, str]) -> tuple[int, str, Path]:
            i, sq = i_sq
            kws = keywords(sq)
            ev = run / f"gather-p{pass_no}-sq{i}.md"
            parts = [f"# Evidence — pass {pass_no}, sub-question {i}", "",
                     f"## Sub-question\n\n{sq}", ""]
            with trace.step(f"gather-p{pass_no}-sq{i}-det", inputs={"subquestion": sq,
                                                                    "keywords": kws}):
                parts.append("## studio map (archetype symptom match)\n```\n"
                             + gather_studio(sq) + "\n```\n")
                parts.append("## studio cards (local tagged corpus)\n```\n"
                             + gather_cards(kws[0] if kws else "system") + "\n```\n")
                parts.append("## knowledge/ library (distilled sources)\n```\n"
                             + gather_knowledge(kws) + "\n```\n")
                if use_recall:
                    parts.append("## Recall KB (optional web layer)\n```\n"
                                 + gather_recall(sq) + "\n```\n")
                else:
                    parts.append("## Recall KB\n\n(not enabled: pass --recall)\n")
                ev.write_text("\n".join(parts))
                trace.set_outputs({"artifact": ev.name, "bytes": ev.stat().st_size})
            return i, sq, ev

        for tup in map(det_gather, enumerate(subs, 1)):
            evidence_files.append(tup)

        if dry:
            for i, sq, ev in evidence_files:
                fj = run / f"findings-p{pass_no}-sq{i}.json"
                fj.write_text(json.dumps({"subquestion": sq, "findings": [],
                                          "dry_run": True}, indent=2) + "\n")
            trace.set_outputs({"findings": 0, "dry_run": True})
            return findings

        def agent_extract(tup: tuple[int, str, Path]) -> list[dict]:
            i, sq, ev = tup
            raw = ev.read_text()[:9000]
            fo = (followups or {}).get(i, "")
            prompt = [
                {"role": "system", "content":
                 "You extract evidence-grounded findings. You never invent sources."},
                {"role": "user", "content":
                 f"Sub-question {i}: {sq}\n"
                 + (f"Follow-up focus for this pass: {fo}\n" if fo else "")
                 + f"\nEvidence gathered (deterministic pulls):\n---\n{raw}\n---\n\n"
"Extract findings that bear on the sub-question, ONLY from the evidence. "
f'Return ONLY JSON: {{"findings": [{{"claim": "...", "quote": "exact or nearest '
f'phrase from evidence", "source": "studio-map|cards|knowledge|recall", '
f'"subquestion": {i}}}]}} '
'(empty list if the evidence is silent — silence is a finding)."}'}]
            try:
                t, usage = llm(prompt, model, timeout, max_tokens=1600)
                trace.llm_call(f"extract-p{pass_no}-sq{i}", model, prompt, t, usage,
                               tags=[f"pass:{pass_no}", f"sq:{i}"])
                fs = extract_json(t).get("findings", [])
            except Exception as exc:  # noqa: BLE001 — degrade honestly
                trace.llm_call(f"extract-p{pass_no}-sq{i}", model, prompt, "",
                               error=str(exc), tags=[f"pass:{pass_no}", f"sq:{i}", "failed"])
                fs = [{"claim": "needs-agent-reasoning (extraction failed: "
                       + str(exc)[:80] + ")",
                       "quote": "", "source": "degraded", "subquestion": i}]
            fj = run / f"findings-p{pass_no}-sq{i}.json"
            fj.write_text(json.dumps({"subquestion": sq, "findings": fs}, indent=2) + "\n")
            return fs

        with ThreadPoolExecutor(max_workers=4) as pool:
            for fs in pool.map(agent_extract, evidence_files):
                findings.extend(fs)
        trace.set_outputs({"findings": len(findings)})
    return findings


def next_followups(run: Path, trace: TraceWriter, subs: list[str], findings: list[dict],
                   pass_no: int, model: str, timeout: int) -> dict[int, str]:
    """LLM proposes per-sub-question follow-up focus for the NEXT pass (gap-driven)."""
    with trace.step(f"gap-queries-p{pass_no}", inputs={"findings": len(findings)}):
        per: dict[int, list[str]] = {i: [] for i in range(1, len(subs) + 1)}
        for f in findings:
            i = f.get("subquestion")
            if isinstance(i, int) and i in per:
                per[i].append(f.get("claim", ""))
        try:
            prompt = [{"role": "user", "content":
                       "Per sub-question below, the claims already gathered. For each, give "
                       "ONE follow-up query angle that would close the biggest evidence gap "
                       "(different vocabulary than the claims use).\n"
                       + "\n".join(f"SQ{i}: {sq}\n  claims: {c or '(none)'}"
                                   for i, (sq, c) in enumerate(zip(subs, per.values()), 1))
                       + '\n\nReturn ONLY JSON: {"followups": [{"sq": 1, "query": "..."}, ...]}'}]
            t, usage = llm(prompt, model, timeout, max_tokens=500)
            trace.llm_call(f"gap-queries-p{pass_no}", model, prompt, t, usage,
                           tags=[f"pass:{pass_no}", "gaps"])
            out = {}
            for item in extract_json(t).get("followups", []):
                try:
                    out[int(item["sq"])] = str(item["query"])[:200]
                except (KeyError, TypeError, ValueError):
                    continue
            trace.set_outputs({"followups": len(out)})
            return out
        except Exception as exc:  # noqa: BLE001 — follow-ups are best-effort
            trace.set_outputs({"error": str(exc)})
            return {}


def phase_verify(run: Path, trace: TraceWriter, findings: list[dict], votes: int,
                 model: str, timeout: int, max_claims: int, dry: bool) -> tuple[dict, bool]:
    art = run / "verify.md"
    with trace.phase("D3-adversarial-verify", inputs={"findings": len(findings),
                                                      "votes": votes}):
        # dedupe claims, deterministic keying
        seen: dict[str, dict] = {}
        for f in findings:
            key = re.sub(r"\W+", " ", f.get("claim", "").lower()).strip()[:70]
            if key and key not in seen:
                seen[key] = f
        claims = list(seen.values())[:max_claims]

        if dry or not claims:
            body = ["# Adversarial verification — refute-default (DRY-RUN / no claims)",
                    "", "## Method", "",
                    f"votes={votes} (dry-run: no LLM votes cast)"
                    if dry else f"votes={votes} — zero claims reached verify", "",
                    "## Claim votes", "",
                    "| # | claim | verdicts | tally | verdict |", "|---|---|---|---|---|",
                    "| - | (none) | - | - | - |", "", "## Verdicts", "",
                    "- " + ("DRY-RUN: verification skipped by design"
                            if dry else "no claims extracted from evidence"), ""]
            art.write_text("\n".join(body))
            trace.set_outputs({"claims": 0, "check": "PASS" if dry else "FAIL"})
            return {}, dry

        def vote_one(arg: tuple[int, dict]) -> list[dict]:
            i, claim = arg
            vs = []
            for v in range(1, votes + 1):
                prompt = [
                    {"role": "system", "content":
                     "You are an adversarial reviewer. Default stance: the claim is WRONG."},
                    {"role": "user", "content":
                     f"Claim {i}: {claim.get('claim','')}\n"
                     f"Alleged evidence: \"{claim.get('quote','')}\" "
                     f"(layer: {claim.get('source','?')})\n\n"
                     "Cross-check the claim against the evidence string and general logic. "
                     "Try to REFUTE it: is it unsupported, over-generalized, or "
                     "contradicted? Only if you cannot refute, mark SUPPORTED.\n"
                     'Return ONLY JSON: {"verdict": "REFUTED|SUPPORTED|UNVERIFIABLE", '
                     '"reason": "<one sentence>"}'}]
                try:
                    t, usage = llm(prompt, model, timeout, max_tokens=600)
                    trace.llm_call(f"verify-c{i}-v{v}", model, prompt, t, usage,
                                   tags=["phase:verify", f"claim:{i}", f"vote:{v}"])
                    d = extract_json(t)
                    vs.append({"verdict": str(d.get("verdict", "UNVERIFIABLE")).upper(),
                               "reason": str(d.get("reason", ""))[:200]})
                except Exception as exc:  # noqa: BLE001 — degrade honestly
                    trace.llm_call(f"verify-c{i}-v{v}", model, prompt, "",
                                   error=str(exc), tags=["phase:verify", "failed"])
                    vs.append({"verdict": "UNVERIFIABLE",
                               "reason": "vote error: " + str(exc)[:80]})
            return vs

        with ThreadPoolExecutor(max_workers=4) as pool:
            all_votes = list(pool.map(vote_one, enumerate(claims, 1)))

        verdicts: dict[str, dict] = {}
        rows = ["| # | claim | verdicts | tally | verdict |", "|---|---|---|---|---|"]
        for i, (claim, vs) in enumerate(zip(claims, all_votes), 1):
            ref = sum(1 for v in vs if v["verdict"] == "REFUTED")
            sup = sum(1 for v in vs if v["verdict"] == "SUPPORTED")
            if ref >= (votes + 1) // 2 or ref > sup:
                verd = "REFUTED"
            elif sup > ref and ref == 0:
                verd = "VERIFIED"
            else:
                verd = "UNVERIFIED"
            verdicts[f"c{i}"] = {"claim": claim, "votes": vs, "verdict": verd}
            rows.append(f"| {i} | {claim.get('claim','')[:70]} | "
                        f"{' / '.join(v['verdict'] for v in vs)} | R{ref}:S{sup} | {verd} |")
        body = ["# Adversarial verification — refute-default", "",
                "## Method", "",
                f"- votes per claim: {votes} (independent, refute-default prompts)",
                f"- model: {model}; claims capped at {max_claims}",
                "- VERIFIED = zero REFUTED and SUPPORTED majority; REFUTED = REFUTED "
                "majority or tie against; else UNVERIFIED", "",
                "## Claim votes", "", *rows, "", "## Verdicts", ""]
        for i in sorted(verdicts, key=lambda k: int(k[1:])):
            v = verdicts[i]
            body.append(f"{int(i[1:])}. **{v['verdict']}** — {v['claim'].get('claim','')}")
            for vv in v["votes"]:
                body.append(f"   - {vv['verdict']}: {vv['reason']}")
        art.write_text("\n".join(body) + "\n")
        ok = "## Claim votes" in "\n".join(body) and "## Verdicts" in "\n".join(body)
        trace.set_outputs({"claims": len(claims), "check": "PASS" if ok else "FAIL"})
    return verdicts, ok


def phase_synthesize(run: Path, trace: TraceWriter, q: str, question_md: str,
                     verdicts: dict, evidence_files: list[Path], model: str,
                     timeout: int, dry: bool, passes: int, votes: int) -> bool:
    art = run / "DELIVERABLE.md"
    with trace.phase("D4-synthesize", inputs={"verdicts": len(verdicts)}):
        ev_head = ""
        for ev in evidence_files[:6]:
            ev_head += f"\n### {ev.name}\n" + ev.read_text(errors="replace")[:1800] + "\n"
        if dry:
            body = ("# Deep-agent DELIVERABLE (DRY-RUN — plumbing proof, no reasoning)\n\n"
                    "## Answer\n\nDRY-RUN: no LLM synthesis ran.\n\n## Evidence\n\n"
                    "- deterministic gather artifacts: see gather-p*.md in this run dir\n\n"
                    "## Refuted or unverified\n\n- DRY-RUN: verification not run\n\n"
                    "## Falsifier\n\n- DRY-RUN: none (no claims made)\n\n"
                    "## Next questions\n\n- re-run without --dry-run\n")
        else:
            vd = "\n".join(f"- [{v['verdict']}] {v['claim'].get('claim','')} "
                           f"(evidence: \"{v['claim'].get('quote','')[:90]}\")"
                           for v in verdicts.values()) or "- (no claims reached verify)"
            prompt = [
                {"role": "system", "content":
                 "You synthesize verified deep-research into a decision-grade deliverable. "
                 "You use ONLY the material given; no new claims; say Unknown where "
                 "evidence is silent."},
                {"role": "user", "content":
                 f"Original question: {q}\n\nRestated brief:\n{question_md[:1200]}\n\n"
                 f"Verified/refuted claims ({votes} adversarial votes each, "
                 f"{passes} gather pass(es)):\n{vd}\n\n"
                 f"Evidence digest:\n{ev_head[:12000]}\n\n"
                 "Write the DELIVERABLE with EXACTLY these sections:\n"
                 "## Answer\n(direct answer to the question, built from VERIFIED claims "
                 "and explicitly marked UNVERIFIED material; Unknown where silent)\n"
                 "## Evidence\n(bulleted claim -> source layer; mark each VERIFIED/"
                 "UNVERIFIED/REFUTED)\n## Refuted or unverified\n(what did not survive "
                 "adversarial voting, and what was never testable)\n## Falsifier\n"
                 "(one observation + a deadline in weeks that would kill this answer)\n"
                 "## Next questions\n(2-3 follow-ups the evidence could not reach)"}]
            try:
                t, usage = llm(prompt, model, timeout, max_tokens=2000)
                trace.llm_call("synthesize-deliverable", model, prompt, t, usage,
                               tags=["phase:synthesize"])
                body = t
            except Exception as exc:  # noqa: BLE001 — degrade honestly
                trace.llm_call("synthesize-deliverable", model, prompt, "",
                               error=str(exc), tags=["phase:synthesize", "failed"])
                body = ("# Deep-agent DELIVERABLE (DEGRADED — synthesis LLM failed)\n\n"
                        "## Answer\n\nneeds-agent-reasoning (synthesis call failed: "
                        f"{str(exc)[:100]})\n\n## Evidence\n\n- see gather-*.md artifacts\n\n"
                        "## Refuted or unverified\n\n- unknown (verify.md carries votes)\n\n"
                        "## Falsifier\n\n- none derivable (degraded run)\n\n"
                        "## Next questions\n\n- re-run when the local proxy is up\n")
        art.write_text(body)
        need = ["## Answer", "## Evidence", "## Refuted or unverified",
                "## Falsifier", "## Next questions"]
        ok = all(re.search(r"(?im)^" + re.escape(s), body) for s in need)
        trace.set_outputs({"artifact": art.name, "check": "PASS" if ok else "FAIL"})
    return ok


def write_verify_log(run: Path, trace: TraceWriter, checks: list[tuple[str, bool]],
                     dry: bool) -> bool:
    """D5a: freeze verify.log (checks + presence + verdict). Sealed later, never edited."""
    with trace.phase("D5-seal", inputs={"checks": len(checks)}):
        lines = [f"== deep-agent verify {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}"
                 + (" (DRY-RUN)" if dry else ""), ""]
        ok_all = True
        for name, ok in checks:
            lines.append(f"{'PASS' if ok else 'FAIL'} {name}")
            ok_all &= ok
        for f in sorted(run.glob("*.md")) + sorted(run.glob("*.json")):
            n = len(f.read_text(errors="replace").splitlines())
            lines.append(f"PASS {f.name} ({n} lines)")
        verdict = "GREEN" if ok_all else "RED"
        lines += ["",
                  f"RUN {verdict} — deliverable {run / 'DELIVERABLE.md'}",
                  "ProofPacket: proofpacket.json (seal + integrity transcript in seal.log)",
                  f"re-verify: python3 {STUDIO / 'proofpacket/verify.py'} "
                  f"{run / 'proofpacket.json'}", ""]
        (run / "verify.log").write_text("\n".join(lines))
        trace.set_outputs({"verdict": verdict, "verify_log": "frozen"})
        return ok_all


def execute_seal(run: Path, slug: str, dry: bool, checks: int) -> tuple[bool, str]:
    """D5b: seal every artifact (verify.log + trace.jsonl already final) and prove it."""
    arts = ["problem.txt", "question.md", "decompose.md", "verify.md",
            "DELIVERABLE.md", "verify.log", "trace.jsonl"]
    arts += [p.name for p in sorted(run.glob("gather-*.md"))]
    arts += [p.name for p in sorted(run.glob("findings-*.json"))]
    seal_cmd = [sys.executable, str(STUDIO / "proofpacket/seal.py"),
                "--out", "proofpacket.json", "--name", f"deep-agent-{slug}"[:60],
                "--verifier", "deep-agent-runner",
                "--evidence", ("dry-run plumbing proof" if dry else
                               f"deep loop: {checks} phase checks; "
                               "adversarial votes in verify.md"),
                "--base", str(run)] + arts
    rc, out = run_cmd(seal_cmd, cwd=run)
    rc2, out2 = run_cmd([sys.executable, str(STUDIO / "proofpacket/verify.py"),
                         str(run / "proofpacket.json")])
    packet_ok = rc == 0 and rc2 == 0 and "=== VERIFIED ===" in out2
    packet_sha = ""
    pj = run / "proofpacket.json"
    if pj.is_file():
        try:
            packet_sha = json.loads(pj.read_text()).get("packet_sha256", "")[:16]
        except json.JSONDecodeError:
            pass
    transcript = ["== seal transcript ==", out.strip(), "", out2.strip(), "",
                  ("SEAL VERIFIED" if packet_ok else "SEAL FAILED")
                  + (f" — packet sha256:{packet_sha}" if packet_sha else ""), "",
                  f"deliverable: {run / 'DELIVERABLE.md'}", ""]
    (run / "seal.log").write_text("\n".join(transcript))
    print("\n".join(transcript))
    return packet_ok, packet_sha


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description="Deep Agent Process runner")
    ap.add_argument("question")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-passes", type=int, default=3)
    ap.add_argument("--verify", dest="votes", type=int, default=2)
    ap.add_argument("--model", default="claude-haiku-4-5")
    ap.add_argument("--reason-model", default="claude-sonnet-4-5")
    ap.add_argument("--max-claims", type=int, default=8)
    ap.add_argument("--recall", action="store_true",
                    help="enable optional web layer (studio search / Recall KB)")
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--runs-root", default=None)
    args = ap.parse_args()

    q = args.question.strip()
    if not q:
        print("usage: run.py \"<question>\" [--dry-run] [--max-passes N] [--verify N]")
        return 2

    runs_root = Path(args.runs_root) if args.runs_root else (
        Path.home() / ".rig/systems-studio/runs/deep-agent")
    slug = re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:40] or "run"
    run = runs_root / f"{time.strftime('%Y%m%d-%H%M%S')}-{slug}"
    run.mkdir(parents=True)
    (run / "problem.txt").write_text(q + "\n")

    trace = TraceWriter(run / "trace.jsonl", RUN_TYPE_ROOT,
                        metadata={"dry_run": args.dry_run, "max_passes": args.max_passes,
                                  "votes": args.votes, "studio": str(STUDIO)})
    trace.start()
    print(f"[run] {run}")

    # D0 QUESTION
    qpath, ok_q = phase_question(run, trace, q, args.reason_model, args.timeout, args.dry_run)
    question_md = Path(qpath).read_text()

    # D1 DECOMPOSE
    subs, ok_d = phase_decompose(run, trace, q, question_md, args.reason_model,
                                 args.timeout, args.dry_run)
    print(f"[decompose] {len(subs)} sub-questions")

    # D2 GATHER (bounded passes)
    findings: list[dict] = []
    followups: dict[int, str] = {}
    evidence_files = sorted(run.glob("gather-*.md"))
    for p in range(1, args.max_passes + 1):
        if not args.dry_run and p > 1:
            followups = next_followups(run, trace, subs, findings, p - 1,
                                       args.model, args.timeout)
        findings += gather_pass(run, trace, subs, p, args.model, args.timeout,
                                args.dry_run, args.recall, followups)
        evidence_files = sorted(run.glob("gather-*.md"))
        print(f"[gather] pass {p}/{args.max_passes}: total findings {len(findings)}")
        if args.dry_run:
            break

    # D3 ADVERSARIAL VERIFY
    verdicts, ok_v = phase_verify(run, trace, findings, args.votes, args.model,
                                  args.timeout, args.max_claims, args.dry_run)
    print(f"[verify] {len(verdicts)} claims voted")

    # D4 SYNTHESIZE
    ok_s = phase_synthesize(run, trace, q, question_md, verdicts, evidence_files,
                            args.reason_model, args.timeout, args.dry_run,
                            args.max_passes, args.votes)

    # D5 SEAL — freeze verify.log, close the trace, THEN seal both into the packet.
    checks = [("question.md sections", ok_q), ("decompose.md sections", ok_d),
              ("verify.md sections", ok_v), ("DELIVERABLE.md sections", ok_s)]
    ok_all = write_verify_log(run, trace, checks, args.dry_run)
    trace.finish(outputs={"verdict": "GREEN" if ok_all else "RED",
                          "run_dir": str(run),
                          "deliverable": str(run / "DELIVERABLE.md"),
                          "seal": "proofpacket.json (transcript: seal.log)"})
    packet_ok, packet_sha = execute_seal(run, slug, args.dry_run, len(checks))
    print(f"[trace] {len((run / 'trace.jsonl').read_text().splitlines())} records")
    print(f"[seal] {'VERIFIED' if packet_ok else 'FAILED'}"
          + (f" sha256:{packet_sha}" if packet_sha else ""))
    print(f"run dir: {run}")
    return 0 if (ok_all and packet_ok) else 1


if __name__ == "__main__":
    raise SystemExit(main())
