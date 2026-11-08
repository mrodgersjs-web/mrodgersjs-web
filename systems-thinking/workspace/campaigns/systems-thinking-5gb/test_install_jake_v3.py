#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

MODULE = Path(__file__).with_name("install_jake_v3.py")
spec = importlib.util.spec_from_file_location("installer", MODULE)
installer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(installer)


def test_install_and_reject_short_appendix() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        module = root / "JAKE_SYSTEMS_THINKING.md"
        module.write_text("# Jake\n\nVersion: 2.0.0\n\n## Existing loop\n")
        appendix = root / "appendix.md"
        appendix.write_text(
            "## Sourced mechanism library (OmniScout 36GB, v3)\n\n- cited mechanism\n"
        )
        proof = root / "appendix.proof.json"
        proof.write_text(
            json.dumps(
                {
                    "ok": True,
                    "cards": 12,
                    "sha256": hashlib.sha256(appendix.read_bytes()).hexdigest(),
                }
            )
        )
        result = installer.install(module, appendix, proof, root / "install.proof.json", 12)
        assert result["cards"] == 12
        assert (root / "JAKE_SYSTEMS_THINKING.md.v2-backup-20260829").exists()
        assert "Version: 3.0.0" in module.read_text()
        assert "Sourced mechanism library" in module.read_text()
        base = json.loads(proof.read_text())
        bad = dict(base)
        bad["cards"] = 11
        proof.write_text(json.dumps(bad))
        try:
            installer.install(module, appendix, proof, root / "bad.proof.json", 12)
        except RuntimeError as error:
            assert "need 12" in str(error)
        else:
            raise AssertionError("short appendix was installed")
        curated = dict(base)
        curated.update(
            {
                "cards": 11,
                "source_l2_pass_cards": 12,
                "source_l2_quarantined_cards": 0,
            }
        )
        proof.write_text(json.dumps(curated))
        result = installer.install(
            module, appendix, proof, root / "curated.proof.json", 10
        )
        assert result["cards"] == 11
        assert result["source_l2_pass_cards"] == 12


if __name__ == "__main__":
    test_install_and_reject_short_appendix()
    print("Jake v3 installer tests: PASS")
