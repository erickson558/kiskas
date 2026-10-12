"""Abre el bundle en modo de comprobación y confirma versión y GUI disponibles."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from version import VERSION_LABEL  # noqa: E402


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="kiskas-exe-") as folder:
        report = Path(folder) / "result.json"
        subprocess.run([str(ROOT / "kiskas.exe"), "--self-test", str(report)],
                       cwd=ROOT, check=True, timeout=60)
        result = json.loads(report.read_text(encoding="utf-8"))
        if result.get("status") != "ok" or result.get("version") != VERSION_LABEL:
            raise SystemExit(f"Verificación falló: {result}")
        print(f"Ejecutable verificado: {result}")


if __name__ == "__main__":
    main()
