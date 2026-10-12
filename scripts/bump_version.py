"""Incrementa SemVer y sincroniza los documentos antes del siguiente commit."""

import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def bump(root: Path, part: str, message: str) -> str:
    """Prepara todos los cambios en memoria antes de escribir los archivos."""
    old = (root / "VERSION").read_text(encoding="ascii").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", old):
        raise ValueError("VERSION debe contener major.minor.patch")
    major, minor, patch = map(int, old.split("."))
    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError("Use major, minor o patch")
    new = f"{major}.{minor}.{patch}"
    readme_path = root / "README.md"
    readme, replacements = re.subn(r"Versión: \*\*V\d+\.\d+\.\d+\*\*",
                                  f"Versión: **V{new}**", readme_path.read_text(encoding="utf-8"))
    if replacements != 1:
        raise ValueError("README debe incluir exactamente una línea de versión")
    changelog_path = root / "CHANGELOG.md"
    changelog = changelog_path.read_text(encoding="utf-8")
    marker = "# Changelog\n"
    if not changelog.startswith(marker):
        raise ValueError("CHANGELOG debe empezar con '# Changelog'")
    # La fecha de las versiones se agrega manualmente cuando sea necesaria;
    # así no depende de la zona horaria del equipo que hace la compilación.
    entry = f"\n## V{new}\n\n- {message.strip()}\n"
    changelog = marker + entry + changelog[len(marker):]
    (root / "VERSION").write_text(new + "\n", encoding="ascii")
    readme_path.write_text(readme, encoding="utf-8")
    changelog_path.write_text(changelog, encoding="utf-8")
    return new


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("part", choices=("major", "minor", "patch"))
    parser.add_argument("--message", default="Actualización del proyecto.")
    args = parser.parse_args()
    print(f"V{bump(ROOT, args.part, args.message)}")


if __name__ == "__main__":
    main()
