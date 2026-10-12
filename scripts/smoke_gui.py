"""Verificación real de controles y exportaciones sin dejar una ventana abierta."""

import csv
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from kiskas import DONATION_URL, KiskasApp  # noqa: E402


def main() -> None:
    app = KiskasApp()
    app.withdraw()
    try:
        app.update_idletasks()
        assert app.analysis.count == 7
        assert app.blocks.get() == "5-5-5-5"
        app.count.set("100")
        app.prefix.set("3N")
        app.generate()
        assert len(app.codes) == len(set(app.codes)) == 100
        assert all(code.startswith("3N") for code in app.codes)
        assert "combinaciones únicas" in app.status.cget("text")
        app.copy()
        assert app.clipboard_get().splitlines() == app.codes
        app.language.set("English")
        app.refresh_language()
        assert "Combination generator" in app.title()
        assert "Observed alphabet" in app.analysis_text.get("1.0", "end")
        assert "copied to the clipboard" in app.status.cget("text")
        with tempfile.TemporaryDirectory(prefix="kiskas-smoke-") as folder:
            txt, csv_path = Path(folder) / "codes.txt", Path(folder) / "codes.csv"
            app.save_codes(txt)
            app.save_codes(csv_path)
            assert txt.read_text(encoding="utf-8").splitlines() == app.codes
            with csv_path.open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.reader(stream))
            assert rows == [["code"]] + [[code] for code in app.codes]
        with patch("kiskas.messagebox.showerror") as error:
            app.count.set("10001")
            app.generate()
            assert error.call_count == 1
            assert "integer between 1 and 10000" in error.call_args.args[1]
            assert len(app.codes) == 100
            app.count.set("1")
            app.alphabet.set("ß")
            app.generate()
            assert error.call_count == 2
            assert "ASCII" in error.call_args.args[1]
        with patch("kiskas.webbrowser.open", return_value=True) as browser:
            app.donate()
            browser.assert_called_once_with(DONATION_URL)
        with patch("kiskas.filedialog.asksaveasfilename", return_value="unused.txt"), \
                patch.object(app, "save_codes", side_effect=PermissionError("Denied")), \
                patch("kiskas.messagebox.showerror") as error:
            app.export()
            assert "Could not save" in error.call_args.args[1]
        app.language.set("Español")
        app.refresh_language()
        assert "Generador de combinaciones" in app.title()
        print("GUI OK: análisis, generación, idiomas, portapapeles, TXT, CSV, límites y enlace.")
    finally:
        app.destroy()


if __name__ == "__main__":
    main()
