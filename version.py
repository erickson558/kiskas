"""Versión compartida por la interfaz, compilación y automatización."""

from pathlib import Path
import re

# PyInstaller incluye VERSION junto a este módulo dentro del ejecutable.
VERSION = Path(__file__).with_name("VERSION").read_text(encoding="ascii").strip()
if not re.fullmatch(r"\d+\.\d+\.\d+", VERSION):
    raise ValueError("VERSION debe contener major.minor.patch")
VERSION_LABEL = f"V{VERSION}"
