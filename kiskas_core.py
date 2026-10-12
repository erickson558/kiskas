"""Análisis de formato y generación local de combinaciones alfanuméricas.

Los ejemplos permiten observar un formato, no deducir un algoritmo de licencias
ni confirmar que una combinación sea válida en algún servicio externo.
"""

from collections import Counter
from dataclasses import dataclass
import re
import secrets


SAMPLE_CODES = (
    "3N6A2-BX51N-2ZWFY-65DH1",
    "3N7XE-33YAW-44TYW-9UYSC",
    "3N9TZ-TCXPM-TXWPR-VDCTR",
    "3NA8M-7EXTH-1X6PH-FRMJG",
    "3NBT8-G9TXD-61W7B-PR554",
    "553ST-5G8Z7-992M7-D4DTE",
    "59JKZ-SJ6CE-11MZE-5MPCR",
)

# Es una elección configurable: no se infiere que todos estos caracteres estén
# permitidos por el sistema que produjo las muestras. Excluye 0, I y O.
DEFAULT_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZ"
MAX_CODES = 10_000
MAX_TEXT_BYTES = 1_048_576
MAX_BLOCKS = 32
MAX_BLOCK_LENGTH = 32
MAX_TOTAL_LENGTH = 200
_CODE_PATTERN = re.compile(r"[A-Z0-9]+(?:-[A-Z0-9]+)*", flags=re.ASCII)


class PatternError(ValueError):
    """Error traducible por clave, compatible con clientes que usan ValueError.

    El mensaje conserva la explicación española; key y details permiten a la
    interfaz elegir idioma sin interpretar ni reemplazar fragmentos del mensaje.
    """

    def __init__(self, message: str, key: str, **details):
        super().__init__(message)
        self.key: str = key
        self.details: dict = details


@dataclass(frozen=True)
class PatternAnalysis:
    """Observaciones de las muestras; las posiciones variables se marcan con ?."""

    block_lengths: tuple[int, ...]
    alphabet: str
    count: int
    duplicates: int
    position_template: str
    common_prefix: str
    total_length: int
    character_frequencies: dict[str, int]


def _validate_block_lengths(block_lengths: tuple[int, ...]) -> tuple[int, ...]:
    """Comprueba límites antes de calcular capacidad o reservar memoria."""
    if not isinstance(block_lengths, tuple):
        raise PatternError("Las longitudes de los bloques deben ser una tupla.", "core_blocks_type")
    if not 1 <= len(block_lengths) <= MAX_BLOCKS:
        raise PatternError("Debe haber entre 1 y 32 bloques.", "core_blocks_count")
    if any(type(length) is not int or not 1 <= length <= MAX_BLOCK_LENGTH
           for length in block_lengths):
        raise PatternError("Cada bloque debe tener entre 1 y 32 caracteres.", "core_block_length")
    if sum(block_lengths) > MAX_TOTAL_LENGTH:
        raise PatternError("La longitud total sin guiones no puede superar 200.", "core_total_length")
    return block_lengths


def analyze_codes(text: str) -> PatternAnalysis:
    """Analiza líneas de códigos, ignorando líneas vacías y espacios externos.

    Se aceptan minúsculas convirtiéndolas a mayúsculas. Todas las muestras deben
    compartir el mismo formato. Frecuencias y cantidad incluyen duplicados.
    """
    if not isinstance(text, str):
        raise PatternError("Las muestras deben proporcionarse como texto.", "core_samples_type")
    if len(text) > MAX_TEXT_BYTES or len(text.encode("utf-8")) > MAX_TEXT_BYTES:
        raise PatternError("El texto de muestras no puede superar 1 MB.", "core_samples_size")
    lines = text.splitlines()
    if len(lines) > MAX_CODES:
        raise PatternError("El texto no puede contener más de 10000 líneas.", "core_samples_lines")

    # Valida el texto antes de normalizar para no convertir símbolos Unicode en
    # caracteres ASCII que parezcan muestras originales.
    codes = []
    block_lengths = None
    for line_number, line in enumerate(lines, start=1):
        code = line.strip()
        if not code:
            continue
        if not code.isascii() or not _CODE_PATTERN.fullmatch(code.upper()):
            raise PatternError(
                f"Línea {line_number}: use letras A-Z, dígitos y guiones entre bloques.",
                "core_sample_characters", line=line_number,
            )
        code = code.upper()
        current_lengths = _validate_block_lengths(tuple(map(len, code.split("-"))))
        if block_lengths is None:
            block_lengths = current_lengths
        elif current_lengths != block_lengths:
            raise PatternError(f"Línea {line_number}: el formato de bloques es diferente.",
                               "core_sample_format", line=line_number)
        codes.append(code)
    if not codes:
        raise PatternError("Introduzca al menos una combinación para analizar.", "core_samples_empty")

    # Una posición fija solo significa que coincide en las muestras disponibles.
    template = "".join(column[0] if len(set(column)) == 1 else "?"
                       for column in zip(*codes))
    flattened = [code.replace("-", "") for code in codes]
    common_prefix = ""
    for column in zip(*flattened):
        if len(set(column)) != 1:
            break
        common_prefix += column[0]
    frequencies = Counter("".join(flattened))
    observed_alphabet = "".join(sorted(frequencies))
    return PatternAnalysis(
        block_lengths=block_lengths,
        alphabet=observed_alphabet,
        count=len(codes),
        duplicates=len(codes) - len(set(codes)),
        position_template=template,
        common_prefix=common_prefix,
        total_length=sum(block_lengths),
        character_frequencies={character: frequencies[character]
                               for character in observed_alphabet},
    )


def generate_codes(
    count: int,
    block_lengths: tuple[int, ...] = (5, 5, 5, 5),
    alphabet: str = DEFAULT_ALPHABET,
    prefix: str = "",
) -> list[str]:
    """Genera combinaciones únicas; el prefijo ocupa posiciones sin guiones.

    Usa aleatoriedad del sistema mediante secrets. La generación no consulta
    ningún sistema externo ni prueba activación, existencia o validez de códigos.
    """
    if type(count) is not int or not 1 <= count <= MAX_CODES:
        raise PatternError("La cantidad debe ser un entero entre 1 y 10000.", "core_count")
    lengths = _validate_block_lengths(block_lengths)
    if (not isinstance(alphabet, str) or not alphabet
            or not alphabet.isascii()
            or not re.fullmatch(r"[A-Z0-9]+", alphabet, flags=re.ASCII)):
        raise PatternError("El alfabeto debe contener letras A-Z y/o dígitos, en mayúsculas.",
                           "core_alphabet_characters")
    if len(set(alphabet)) != len(alphabet):
        raise PatternError("El alfabeto no puede contener caracteres repetidos.", "core_alphabet_duplicates")
    if not isinstance(prefix, str) or any(character not in alphabet for character in prefix):
        raise PatternError("El prefijo solo puede contener caracteres del alfabeto, sin guiones.",
                           "core_prefix_characters")
    total_length = sum(lengths)
    if len(prefix) > total_length:
        raise PatternError("El prefijo no puede superar la longitud total sin guiones.", "core_prefix_length")
    free_length = total_length - len(prefix)
    base = len(alphabet)
    capacity = base ** free_length
    if count > capacity:
        raise PatternError(f"Solo existen {capacity} combinaciones únicas con estas opciones.",
                           "core_capacity", capacity=capacity)

    # Barajado parcial de índices virtuales: no reserva toda la capacidad y no
    # repite intentos al acercarse a llenarla. El coste es proporcional a count.
    remaining = capacity
    swaps = {}
    result = []
    for _ in range(count):
        selected = secrets.randbelow(remaining)
        value = swaps.get(selected, selected)
        remaining -= 1
        swaps[selected] = swaps.get(remaining, remaining)
        swaps.pop(remaining, None)

        # Cada índice representa una combinación en base len(alphabet), incluidos
        # sus ceros iniciales; después se insertan los separadores por bloque.
        suffix = [alphabet[0]] * free_length
        for position in range(free_length - 1, -1, -1):
            value, digit = divmod(value, base)
            suffix[position] = alphabet[digit]
        characters = prefix + "".join(suffix)
        blocks = []
        offset = 0
        for length in lengths:
            blocks.append(characters[offset:offset + length])
            offset += length
        result.append("-".join(blocks))
    return result
