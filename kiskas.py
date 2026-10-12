"""Interfaz de escritorio bilingüe para analizar y generar combinaciones."""

from __future__ import annotations

import csv
import argparse
import json
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk
import webbrowser

from kiskas_core import DEFAULT_ALPHABET, SAMPLE_CODES, PatternError, analyze_codes, generate_codes
from version import VERSION_LABEL

DONATION_URL = "https://www.paypal.com/donate/?hosted_button_id=ZABFRXC2P3JQN"

# Las traducciones viven en un solo lugar para conservar la misma funcionalidad.
TEXT = {
    "es": {
        "title": "Kiskas · Generador de combinaciones",
        "intro": "Analiza ejemplos y crea combinaciones con el mismo formato.",
        "notice": "Coincidir con el formato no garantiza validez en otros sistemas.",
        "language": "Idioma / Language", "samples": "Ejemplos para analizar",
        "analyze": "Analizar patrón", "restore": "Cargar ejemplos originales",
        "settings": "Configuración de generación", "count": "Cantidad (1–10 000)",
        "blocks": "Tamaño de bloques (ej.: 5-5-5-5)", "alphabet": "Caracteres permitidos",
        "prefix": "Prefijo opcional (sin guiones)", "generate": "Generar combinaciones",
        "results": "Combinaciones generadas", "copy": "Copiar todas",
        "export": "Exportar TXT / CSV", "beer": "Cómprame una cerveza",
        "empty": "Primero genera combinaciones.", "error": "Revisa los datos",
        "count_error": "La cantidad debe ser un número entero entre 1 y 10 000.",
        "blocks_error": "Usa tamaños enteros separados por guiones: 5-5-5-5.",
        "ascii_error": "El alfabeto y el prefijo deben usar letras A-Z o dígitos ASCII.",
        "core_blocks_type": "Las longitudes de los bloques deben ser una tupla.",
        "core_blocks_count": "Debe haber entre 1 y 32 bloques.",
        "core_block_length": "Cada bloque debe tener entre 1 y 32 caracteres.",
        "core_total_length": "La longitud total sin guiones no puede superar 200.",
        "core_samples_type": "Las muestras deben proporcionarse como texto.",
        "core_samples_size": "El texto de muestras no puede superar 1 MB.",
        "core_samples_lines": "El texto no puede contener más de 10000 líneas.",
        "core_sample_characters": "Línea {line}: use letras A-Z, dígitos y guiones entre bloques.",
        "core_sample_format": "Línea {line}: el formato de bloques es diferente.",
        "core_samples_empty": "Introduzca al menos una combinación para analizar.",
        "core_count": "La cantidad debe ser un entero entre 1 y 10000.",
        "core_alphabet_characters": "El alfabeto debe contener letras A-Z y/o dígitos, en mayúsculas.",
        "core_alphabet_duplicates": "El alfabeto no puede contener caracteres repetidos.",
        "core_prefix_characters": "El prefijo solo puede contener caracteres del alfabeto, sin guiones.",
        "core_prefix_length": "El prefijo no puede superar la longitud total sin guiones.",
        "core_capacity": "Solo existen {capacity} combinaciones únicas con estas opciones.",
        "ready": "Listo. El alfabeto observado se puede ajustar.",
        "generated": "{count:,} combinaciones únicas en este lote.",
        "copied": "Combinaciones copiadas al portapapeles.",
        "saved": "Archivo guardado: {path}", "save_title": "Guardar combinaciones",
        "txt": "Texto", "csv": "CSV", "code": "codigo",
        "summary": "Muestras: {count} · Repetidas: {duplicates}\nBloques: {blocks} · Caracteres sin guiones: {length}\nAlfabeto observado: {alphabet}\nPosiciones fijas (? = variable): {template}\nPrefijo común: {prefix}\nFrecuencias: {frequencies}",
        "none": "ninguno", "invalid": "Entrada inválida: {detail}",
        "io_error": "No se pudo guardar: {detail}",
        "clipboard_error": "No se pudo copiar: {detail}",
        "browser_error": "No se pudo abrir el navegador: {detail}",
    },
    "en": {
        "title": "Kiskas · Combination generator",
        "intro": "Analyze examples and create combinations with the same format.",
        "notice": "Matching the format does not guarantee validity in other systems.",
        "language": "Idioma / Language", "samples": "Examples to analyze",
        "analyze": "Analyze pattern", "restore": "Load original examples",
        "settings": "Generation settings", "count": "Count (1–10,000)",
        "blocks": "Block sizes (e.g. 5-5-5-5)", "alphabet": "Allowed characters",
        "prefix": "Optional prefix (without hyphens)", "generate": "Generate combinations",
        "results": "Generated combinations", "copy": "Copy all",
        "export": "Export TXT / CSV", "beer": "Buy me a beer",
        "empty": "Generate combinations first.", "error": "Check your input",
        "count_error": "Count must be an integer between 1 and 10,000.",
        "blocks_error": "Use integer sizes separated by hyphens: 5-5-5-5.",
        "ascii_error": "The alphabet and prefix must use ASCII letters A-Z or digits.",
        "core_blocks_type": "Block lengths must be a tuple.",
        "core_blocks_count": "There must be between 1 and 32 blocks.",
        "core_block_length": "Each block must contain between 1 and 32 characters.",
        "core_total_length": "The total length excluding hyphens cannot exceed 200.",
        "core_samples_type": "Samples must be provided as text.",
        "core_samples_size": "Sample text cannot exceed 1 MB.",
        "core_samples_lines": "Text cannot contain more than 10000 lines.",
        "core_sample_characters": "Line {line}: use letters A-Z, digits, and hyphens between blocks.",
        "core_sample_format": "Line {line}: the block format is different.",
        "core_samples_empty": "Enter at least one combination to analyze.",
        "core_count": "Quantity must be an integer between 1 and 10000.",
        "core_alphabet_characters": "The alphabet must contain uppercase letters A-Z and/or digits.",
        "core_alphabet_duplicates": "The alphabet cannot contain repeated characters.",
        "core_prefix_characters": "The prefix may only contain characters from the alphabet, without hyphens.",
        "core_prefix_length": "The prefix cannot exceed the total length excluding hyphens.",
        "core_capacity": "Only {capacity} unique combinations exist with these options.",
        "ready": "Ready. You can adjust the observed alphabet.",
        "generated": "{count:,} unique combinations in this batch.",
        "copied": "Combinations copied to the clipboard.",
        "saved": "File saved: {path}", "save_title": "Save combinations",
        "txt": "Text", "csv": "CSV", "code": "code",
        "summary": "Samples: {count} · Duplicates: {duplicates}\nBlocks: {blocks} · Characters without hyphens: {length}\nObserved alphabet: {alphabet}\nFixed positions (? = variable): {template}\nCommon prefix: {prefix}\nFrequencies: {frequencies}",
        "none": "none", "invalid": "Invalid input: {detail}",
        "io_error": "Could not save: {detail}",
        "clipboard_error": "Could not copy: {detail}",
        "browser_error": "Could not open the browser: {detail}",
    },
}


class KiskasApp(tk.Tk):
    """Ventana principal; los datos y las reglas se delegan al motor independiente."""

    def __init__(self) -> None:
        super().__init__()
        # Ajusta la ventana a la pantalla y deja margen para barra de tareas/título.
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        width, height = min(1000, screen_width - 80), min(880, screen_height - 160)
        self.geometry(f"{width}x{height}+40+20")
        self.minsize(min(800, width), min(650, height))
        self.language = tk.StringVar(value="Español")
        self.count = tk.StringVar(value="100")
        self.blocks = tk.StringVar(value="5-5-5-5")
        self.alphabet = tk.StringVar(value=DEFAULT_ALPHABET)
        self.prefix = tk.StringVar()
        self.codes: list[str] = []
        self.analysis = None
        self.status_key = "ready"
        self.status_args: dict = {}
        self.translated_widgets: list[tuple[tk.Widget, str]] = []
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        style = ttk.Style(self)
        if "vista" in style.theme_names():
            style.theme_use("vista")

        # El icono empaquetado se busca dentro del bundle o junto al código fuente.
        icon = Path(getattr(sys, "_MEIPASS", Path(__file__).parent)) / "Download_26386.ico"
        try:
            self.iconbitmap(str(icon))
        except tk.TclError:
            pass  # Fuera de Windows o sin icono, la interfaz sigue funcionando.
        self._build_ui()
        self.restore_samples()
        self.refresh_language()

    def tr(self, key: str, **kwargs) -> str:
        lang = "en" if self.language.get() == "English" else "es"
        return TEXT[lang][key].format(**kwargs)

    def error_detail(self, error: ValueError) -> str:
        if isinstance(error, PatternError):
            return self.tr(error.key, **error.details)
        return str(error)

    def _text_widget(self, kind, parent, key, **kwargs):
        widget = kind(parent, **kwargs)
        self.translated_widgets.append((widget, key))
        return widget

    def _build_ui(self) -> None:
        """Construye controles; conserva referencias para traducir sin perder datos."""
        frame = ttk.Frame(self, padding=18)
        frame.grid(sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(7, weight=1)
        header = ttk.Frame(frame)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text=f"Kiskas {VERSION_LABEL}", font=("Segoe UI", 20, "bold")).grid(row=0, column=0, sticky="w")
        self._text_widget(ttk.Label, header, "language").grid(row=0, column=1, padx=8)
        language = ttk.Combobox(header, textvariable=self.language, values=("Español", "English"), state="readonly", width=12)
        language.grid(row=0, column=2)
        language.bind("<<ComboboxSelected>>", lambda event: self.refresh_language())
        self._text_widget(ttk.Label, frame, "intro").grid(row=1, column=0, sticky="w", pady=(4, 0))
        self._text_widget(ttk.Label, frame, "notice", foreground="#8c4800").grid(row=2, column=0, sticky="w", pady=(2, 10))

        examples = self._text_widget(ttk.LabelFrame, frame, "samples", padding=8)
        examples.grid(row=3, column=0, sticky="ew")
        examples.columnconfigure(0, weight=1)
        self.samples_text = scrolledtext.ScrolledText(examples, height=7, font=("Consolas", 10), wrap="none")
        self.samples_text.grid(row=0, column=0, columnspan=2, sticky="ew")
        self._text_widget(ttk.Button, examples, "analyze", command=self.analyze).grid(row=1, column=0, sticky="w", pady=(6, 0))
        self._text_widget(ttk.Button, examples, "restore", command=self.restore_samples).grid(row=1, column=1, sticky="e", pady=(6, 0))
        self.analysis_text = scrolledtext.ScrolledText(frame, height=6, font=("Consolas", 9), wrap="word", state="disabled", background="#f4f5f7")
        self.analysis_text.grid(row=4, column=0, sticky="ew", pady=8)

        settings = self._text_widget(ttk.LabelFrame, frame, "settings", padding=8)
        settings.grid(row=5, column=0, sticky="ew")
        settings.columnconfigure(1, weight=1)
        for row, (key, var) in enumerate((("count", self.count), ("blocks", self.blocks), ("alphabet", self.alphabet), ("prefix", self.prefix))):
            self._text_widget(ttk.Label, settings, key).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=3)
            ttk.Entry(settings, textvariable=var, font=("Consolas", 10)).grid(row=row, column=1, sticky="ew", pady=3)
        self._text_widget(ttk.Button, settings, "generate", command=self.generate).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        self._text_widget(ttk.Label, frame, "results").grid(row=6, column=0, sticky="w", pady=(10, 3))
        self.output = scrolledtext.ScrolledText(frame, height=8, font=("Consolas", 11), wrap="none", state="disabled")
        self.output.grid(row=7, column=0, sticky="nsew")
        buttons = ttk.Frame(frame)
        buttons.grid(row=8, column=0, sticky="ew", pady=(8, 0))
        buttons.columnconfigure(2, weight=1)
        self._text_widget(ttk.Button, buttons, "copy", command=self.copy).grid(row=0, column=0, padx=(0, 8))
        self._text_widget(ttk.Button, buttons, "export", command=self.export).grid(row=0, column=1)
        self._text_widget(ttk.Button, buttons, "beer", command=self.donate).grid(row=0, column=3)
        self.status = ttk.Label(frame, wraplength=920)
        self.status.grid(row=9, column=0, sticky="ew", pady=(8, 0))

    @staticmethod
    def _replace_text(widget, value: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value)
        widget.configure(state="disabled")

    def set_status(self, key: str, **kwargs) -> None:
        self.status_key, self.status_args = key, kwargs
        self.status.configure(text=self.tr(key, **kwargs))

    def refresh_language(self) -> None:
        self.title(f"{self.tr('title')} {VERSION_LABEL}")
        for widget, key in self.translated_widgets:
            widget.configure(text=self.tr(key))
        self.set_status(self.status_key, **self.status_args)
        self.show_analysis()

    def restore_samples(self) -> None:
        self.samples_text.delete("1.0", "end")
        self.samples_text.insert("1.0", "\n".join(SAMPLE_CODES))
        self.analyze()

    def show_analysis(self) -> None:
        if self.analysis is None:
            return
        item = self.analysis
        text = self.tr("summary", count=item.count, duplicates=item.duplicates,
                       blocks="-".join(map(str, item.block_lengths)), length=item.total_length,
                       alphabet=item.alphabet, template=item.position_template,
                       prefix=item.common_prefix or self.tr("none"),
                       frequencies=" · ".join(f"{k}:{v}" for k, v in item.character_frequencies.items()))
        self._replace_text(self.analysis_text, text)

    def analyze(self) -> None:
        """Aplica únicamente formato y alfabeto observados; el prefijo sigue opcional."""
        try:
            analysis = analyze_codes(self.samples_text.get("1.0", "end-1c"))
        except ValueError as exc:
            messagebox.showerror(self.tr("error"), self.tr("invalid", detail=self.error_detail(exc)), parent=self)
            return
        self.analysis = analysis
        self.blocks.set("-".join(map(str, analysis.block_lengths)))
        self.alphabet.set(analysis.alphabet)
        self.show_analysis()

    def generate(self) -> None:
        """Valida entradas de la GUI antes de pedir un lote completo al motor."""
        try:
            if not self.count.get().strip().isascii() or not self.count.get().strip().isdecimal():
                raise ValueError(self.tr("count_error"))
            parts = self.blocks.get().strip().split("-")
            if not all(part.isascii() and part.isdecimal() and len(part) <= 2 for part in parts):
                raise ValueError(self.tr("blocks_error"))
            # No convertir símbolos Unicode a ASCII por accidente (p. ej. ß -> SS).
            if not self.alphabet.get().isascii() or not self.prefix.get().isascii():
                raise ValueError(self.tr("ascii_error"))
            self.codes = generate_codes(int(self.count.get()), tuple(map(int, parts)),
                                        self.alphabet.get().strip().upper(), self.prefix.get().strip().upper())
        except ValueError as exc:
            messagebox.showerror(self.tr("error"), self.tr("invalid", detail=self.error_detail(exc)), parent=self)
            return
        self._replace_text(self.output, "\n".join(self.codes))
        self.set_status("generated", count=len(self.codes))

    def copy(self) -> None:
        if not self.codes:
            self.set_status("empty")
            return
        try:
            self.clipboard_clear()
            self.clipboard_append("\n".join(self.codes))
            self.set_status("copied")
        except tk.TclError as exc:
            messagebox.showerror(self.tr("error"), self.tr("clipboard_error", detail=str(exc)), parent=self)

    def export(self) -> None:
        """El diálogo pide autorización para reemplazar archivos existentes."""
        if not self.codes:
            self.set_status("empty")
            return
        path = filedialog.asksaveasfilename(parent=self, title=self.tr("save_title"),
                                           defaultextension=".txt", initialfile="combinaciones.txt",
                                           filetypes=((self.tr("txt"), "*.txt"), (self.tr("csv"), "*.csv")))
        if path:
            try:
                self.save_codes(Path(path))
                self.set_status("saved", path=path)
            except OSError as exc:
                messagebox.showerror(self.tr("error"), self.tr("io_error", detail=str(exc)), parent=self)

    def save_codes(self, path: Path) -> None:
        """CSV de una columna o TXT UTF-8; los códigos no pueden incluir fórmulas."""
        if path.suffix.lower() == ".csv":
            with path.open("w", encoding="utf-8-sig", newline="") as stream:
                writer = csv.writer(stream)
                writer.writerow([self.tr("code")])
                writer.writerows([code] for code in self.codes)
        else:
            path.write_text("\n".join(self.codes) + "\n", encoding="utf-8")

    def donate(self) -> None:
        # Se abre únicamente el enlace fijo solicitado y solo al pulsar el botón.
        try:
            if not webbrowser.open(DONATION_URL):
                raise OSError("Browser unavailable / Navegador no disponible")
        except OSError as exc:
            messagebox.showerror(self.tr("error"), self.tr("browser_error", detail=str(exc)), parent=self)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", type=Path, metavar="REPORT",
                        help="Verificar el ejecutable sin mostrar ventana y guardar reporte JSON.")
    args = parser.parse_args()
    app = KiskasApp()
    if args.self_test:
        # Comprueba que el bundle contiene motor, VERSION y Tcl/Tk funcionales.
        app.withdraw()
        try:
            app.update_idletasks()
            app.count.set("25")
            app.generate()
            assert app.analysis.count == 7
            assert len(app.codes) == len(set(app.codes)) == 25
            assert all(tuple(map(len, code.split("-"))) == (5, 5, 5, 5) for code in app.codes)
            app.language.set("English")
            app.refresh_language()
            assert "Combination generator" in app.title()
            args.self_test.write_text(json.dumps({"version": VERSION_LABEL, "codes": len(app.codes),
                                                  "tk": tk.TkVersion, "status": "ok"}), encoding="utf-8")
        finally:
            app.destroy()
        return
    app.mainloop()


if __name__ == "__main__":
    main()
