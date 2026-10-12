"""Genera la entrega completa en el orden solicitado usando los archivos reales."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from version import VERSION_LABEL  # noqa: E402


def main() -> None:
    # Es un artefacto generado; los documentos originales se mantienen en Git.
    files = (
        "README.md", "CHANGELOG.md", "requirements.txt", "requirements-build.txt", "LICENSE", "VERSION",
        "version.py", ".github/workflows/release.yml", ".gitignore", ".gitattributes",
        "scripts/build.py", "scripts/bump_version.py", "scripts/smoke_gui.py",
        "scripts/verify_exe.py", "scripts/write_deliverables.py", "AGENTS.md", ".agents/skills/kiskas-sdd/SKILL.md",
        ".agents/skills/kiskas-release/SKILL.md", ".agents/skills/kiskas-comentarios/SKILL.md",
        "docs/spec.md", "docs/plan.md", "docs/tasks.md", "docs/security.md",
        "kiskas.py", "kiskas_core.py", "tests/test_core.py", "tests/test_versioning.py",
    )
    chunks = [f"# Entrega de kiskas {VERSION_LABEL}\n\n",
              "Generada desde los archivos de esta versión. Los documentos originales son la fuente mantenida.\n\n",
              "## 1. Análisis inicial\n\n",
              "La carpeta original solo contenía un icono. Se creó una aplicación Tkinter, motor probado, documentación SDD, skills, licencia, versionado, compilación y workflow de GitHub.\n\n",
              "Las siete muestras tienen cuatro bloques de cinco caracteres; cinco comienzan por 3N, pero ese prefijo no es común a todas. No hay posiciones de caracteres fijas entre las siete. Las muestras no permiten reconstruir un algoritmo privado ni garantizar validez en otros sistemas. El alfabeto observado se distingue del elegido por el usuario.\n\n",
              "Se utiliza la cuenta erickson558 y el repositorio público erickson558/kiskas, según el encargo. Las verificaciones reales y sus límites figuran en docs/tasks.md y docs/security.md.\n\n",
              "## 2. Estrategia de versionado recomendada\n\n",
              f"La versión actual es {VERSION_LABEL}; VERSION contiene SemVer sin la V. El primer commit usa V1.0.0. Incrementar patch para correcciones o documentación relevante, minor para funciones compatibles y major para incompatibilidades. Cada commit relevante actualiza versión y changelog antes del push. scripts/bump_version.py sincroniza los documentos; la aplicación, metadata del exe, tag y release leen la misma versión. GitHub rechaza una revisión que intente reutilizar un tag.\n\n",
              "## 3. Archivos creados\n\n",
              "\n".join(f"- `{name}`" for name in files),
              "\n\nTambién se conserva Download_26386.ico y se incluye docs/COMANDOS.md y el entorno de build local excluido de Git.\n\n",
              "## 4. Contenido completo de los archivos\n\n"]
    for name in files:
        suffix = Path(name).suffix
        language = {".py": "python", ".yml": "yaml", ".md": "markdown"}.get(suffix, "text")
        # Cuatro acentos protegen bloques Markdown de tres acentos en el README.
        chunks.append(f"### {name}\n\n````{language}\n{(ROOT / name).read_text(encoding='utf-8').rstrip()}\n````\n\n")
    chunks.extend(["## 5. Comandos paso a paso\n\n", (ROOT / "docs/COMANDOS.md").read_text(encoding="utf-8"),
                   "\n\n## 6. Instrucciones de compilación\n\n",
                   "Desde la raíz, en Windows y con Python 3.12:\n\n```powershell\npy -3.12 -m venv .venv\n.\\.venv\\Scripts\\python.exe -m pip install -r requirements-build.txt\n.\\.venv\\Scripts\\python.exe scripts/build.py\n.\\.venv\\Scripts\\python.exe scripts/verify_exe.py\n```\n\n",
                   "El script ejecuta PyInstaller con --onefile --windowed --noupx --icon Download_26386.ico, recursos de versión y VERSION empaquetado. Usa rutas absolutas y --distpath para crear kiskas.exe junto a kiskas.py. También genera SHA256SUMS.txt y este documento. La verificación abre el bundle en modo diagnóstico, confirma Tcl/Tk y generación y termina automáticamente. El usuario abre kiskas.exe normalmente para utilizar la GUI.\n"])
    path = ROOT / "ENTREGA.md"
    path.write_text("".join(chunks), encoding="utf-8")
    print(f"Entrega completa: {path}")


if __name__ == "__main__":
    main()
