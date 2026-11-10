# YouTube Knowledge Cards — Manifest

Scraped: 2026-08-28
Studio: systems-thinking-studio
Method: yt-dlp auto-captions (`--skip-download --write-auto-subs --sub-langs "en.*" --sub-format vtt/srt`), VTT→timestamped-text conversion, then per-video distillation into knowledge cards. Raw subtitle text kept in `raw/<id>.txt` for provenance.

## Counts

| Metric | Count |
|---|---|
| Corpus YouTube videos matching filter (tags: systems-thinking/psychology/strategy AND youtube.com source) | 80 |
| Taken from corpus (top 12 by title length, 1 duplicate series re-upload skipped) | 12 |
| Canon search queries run (`ytsearch`: Meadows, Senge, Ackoff, Goldratt, archetypes, stocks/flows) | 6 |
| Taken from canon searches (top 1–2 each, no duplicates) | 8 |
| **Scraped OK (cards + raw text)** | **20** |
| Skipped — no usable English subtitles | 0 |
| Skipped — garbage subtitles | 0 |
| Hard cap | 20 (reached exactly) |

## Corpus cards (12)

| video_id | channel | title | studio phase |
|---|---|---|---|
| lB8aVGBYD-M | Audiobook Elevate | The Art of Strategic Thinking (win quietly) | frame |
| dRVXSwBnoak | Machiavellian Mind | Become Dangerously Focused — the General's Mindset | ground |
| n4mQg6aNilg | Book Insight | The Elite System to Finish Everything You Start | ground |
| tOFPtiM48qg | Elite Audiobooks | Train Your Brain to Outsmart Any Situation | frame |
| PvcisblLbfE | Productivity Game | How to Think Like a Rocket Scientist (RCKT) | leverage |
| BOydkXrwpm0 | SMQ Audiobook | The Art of Negotiation | leverage |
| _QAVExf_1uw | AI Engineer | Demand-Driven Context | ground |
| ItSLny8on5I | Jovan EEN | The Math Behind "AI Will Replace Engineers" | ground |
| RZIn9tfeQ2I | Big Think | Steven Kotler — the science of effortlessness (flow) | ground |
| rOLmfGg6wX0 | English Achieve | Learn Like a Spy (CIA method) | ground |
| RRgCskx2a0k | SUCCESS CHASERS | Master Yourself — philosophy of Miyamoto Musashi | ground |
| eieYagEYr3k | Andrew | 6 Principles That Make My OpenClaw Agents Think Like a CEO | leverage |

Notes: `QlX1mFqMkOo` ("Train Your Brain… Master Critical Thinking", 81 chars) was skipped as a duplicate-series re-upload of `tOFPtiM48qg`; next-ranked card `eieYagEYr3k` (77) was taken instead.

## Canon cards (8)

| video_id | channel | title | studio phase |
|---|---|---|---|
| 9qL4KxqbrFM | Ashley Hodgson | Thinking in Systems, Ch. 6: Leverage Points in Systems | leverage |
| Fln7GnBNWmo | Academy for Systems Change | Peter Senge, The Fifth Discipline | frame |
| EbLh7rZ3rhU | Awal Premi | Systems Thinking Speech by Dr. Russell Ackoff | frame |
| cnW-OxeQ81c | Goldratt Consulting | The 4 Pillars of Theory of Constraints | leverage |
| W18n8m97uuk | TOCICO | Eli Goldratt on What is the Theory of Constraints? | frame |

| zRmEh-PMvWo | Systems Innovation Network | System Archetypes | diagnose |
| CL0cLpcDESQ | Sustainability Simply Put | Stock Flow Diagram using Bathtub Dynamics | diagnose |
| UL8azVk479M | CLExchange | Introduction to Stock Flow Diagrams | diagnose |

Canon picks per search: Meadows → 9qL4KxqbrFM; Senge → Fln7GnBNWmo (the full 78-min lecture over two short clips); Ackoff → EbLh7rZ3rhU (re-upload duplicates of the same speech skipped); Goldratt → cnW-OxeQ81c + W18n8m97uuk; archetypes → zRmEh-PMvWo; stocks/flows → CL0cLpcDESQ + UL8azVk479M.

## Coverage by studio phase

- **frame**: 5 (Senge, Ackoff, Goldratt-what-is-TOC, Strategic Thinking, Train Your Brain)
- **diagnose**: 3 (System Archetypes, Bathtub Dynamics, Stock Flow Intro)
- **leverage**: 5 (Meadows Leverage Points, TOC 4 Pillars, Rocket Scientist, Negotiation, OpenClaw CEO principles)
- **ground**: 7 (AI-replacement math, Demand-Driven Context, Kotler flow, Learn Like a Spy, Musashi, Machiavelli focus, Finish Everything)

## Distillation runs

| date | attempted | distilled | pending |
|---|---|---|---|
| 2026-08-28 11:52 | 3 | 0 | 3 |
| 2026-08-28 11:53 | 3 | 3 | 0 |
| 2026-08-28 13:08 | 177 | 177 | 0 |
