"""Comprueba que cada incremento mantiene coherencia antes de una release."""

from pathlib import Path
import tempfile
import unittest

from scripts.bump_version import bump


class VersioningTests(unittest.TestCase):
    def test_all_increments_keep_documents_in_sync(self):
        for part, expected in (("major", "2.0.0"), ("minor", "1.3.0"), ("patch", "1.2.4")):
            with self.subTest(part=part), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / "VERSION").write_text("1.2.3\n")
                (root / "README.md").write_text("Versión: **V1.2.3**\n", encoding="utf-8")
                (root / "CHANGELOG.md").write_text("# Changelog\n\n## V1.2.3\n", encoding="utf-8")
                self.assertEqual(bump(root, part, "Cambio comprobado"), expected)
                self.assertEqual((root / "VERSION").read_text().strip(), expected)
                self.assertIn(f"**V{expected}**", (root / "README.md").read_text(encoding="utf-8"))
                self.assertIn(f"## V{expected}\n\n- Cambio comprobado", (root / "CHANGELOG.md").read_text(encoding="utf-8"))

    def test_invalid_document_does_not_partially_change_version(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "VERSION").write_text("1.2.3\n")
            (root / "README.md").write_text("Versión: **V1.2.3**\n", encoding="utf-8")
            (root / "CHANGELOG.md").write_text("Encabezado inválido", encoding="utf-8")
            with self.assertRaises(ValueError):
                bump(root, "patch", "No se debe escribir")
            self.assertEqual((root / "VERSION").read_text().strip(), "1.2.3")
            self.assertIn("V1.2.3", (root / "README.md").read_text(encoding="utf-8"))
