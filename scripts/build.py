"""Compila un ejecutable Windows portátil con icono y versión embebidos."""

from pathlib import Path
import hashlib
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from version import VERSION, VERSION_LABEL  # noqa: E402


def main() -> None:
    if sys.platform != "win32":
        raise SystemExit("El .exe debe compilarse en Windows.")
    parts = tuple(map(int, VERSION.split(".")))
    if any(part > 65535 for part in parts):
        raise SystemExit("Los números de versión de Windows no pueden superar 65535.")
    icon = ROOT / "Download_26386.ico"
    if not icon.is_file():
        raise SystemExit("Falta el icono Download_26386.ico")
    build = ROOT / "build"
    build.mkdir(exist_ok=True)

    # La metadata permite consultar la misma versión en Propiedades de Windows.
    version_file = build / "windows-version.txt"
    numeric = (*parts, 0)
    version_file.write_text(f"""VSVersionInfo(
  ffi=FixedFileInfo(filevers={numeric!r}, prodvers={numeric!r}, mask=0x3f,
    flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[StringFileInfo([StringTable('040904B0', [
    StringStruct('CompanyName', 'erickson558'),
    StringStruct('FileDescription', 'Kiskas combination generator'),
    StringStruct('FileVersion', '{VERSION}'),
    StringStruct('InternalName', 'kiskas'),
    StringStruct('OriginalFilename', 'kiskas.exe'),
    StringStruct('ProductName', 'Kiskas'),
    StringStruct('ProductVersion', '{VERSION_LABEL}'),
    StringStruct('LegalCopyright', 'Copyright 2026 erickson558; Apache-2.0')
  ])]), VarFileInfo([VarStruct('Translation', [1033, 1200])])]
)
""", encoding="utf-8")

    # Una lista de argumentos evita interpretar espacios o metacaracteres del path.
    subprocess.run([
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile",
        "--windowed", "--noupx", "--name", "kiskas", "--distpath", str(ROOT),
        "--workpath", str(build / "pyinstaller"), "--specpath", str(build),
        "--icon", str(icon), "--version-file", str(version_file),
        "--add-data", f"{ROOT / 'VERSION'};.",
        "--add-data", f"{icon};.", str(ROOT / "kiskas.py"),
    ], cwd=ROOT, check=True)
    executable = ROOT / "kiskas.exe"
    digest = hashlib.sha256(executable.read_bytes()).hexdigest()
    (ROOT / "SHA256SUMS.txt").write_text(f"{digest}  kiskas.exe\n", encoding="ascii")
    print(f"Creado: {executable} ({VERSION_LABEL})\nSHA256: {digest}")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "write_deliverables.py")],
                   cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
