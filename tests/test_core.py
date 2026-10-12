"""Pruebas del formato, los límites y el muestreo sin repeticiones."""

import unittest
from unittest.mock import patch

from kiskas_core import DEFAULT_ALPHABET, SAMPLE_CODES, PatternError, analyze_codes, generate_codes


class ErrorContractTests(unittest.TestCase):
    def test_error_preserves_value_error_and_spanish_message(self):
        with self.assertRaises(ValueError) as context:
            generate_codes(0)
        error = context.exception
        self.assertIsInstance(error, PatternError)
        self.assertEqual(error.key, "core_count")
        self.assertEqual(error.details, {})
        self.assertEqual(str(error), "La cantidad debe ser un entero entre 1 y 10000.")

    def test_error_reports_structured_details(self):
        with self.assertRaises(PatternError) as context:
            analyze_codes("AB\nA_")
        self.assertEqual(context.exception.key, "core_sample_characters")
        self.assertEqual(context.exception.details, {"line": 2})
        with self.assertRaises(PatternError) as context:
            analyze_codes("AB\nABC")
        self.assertEqual(context.exception.key, "core_sample_format")
        self.assertEqual(context.exception.details, {"line": 2})
        with self.assertRaises(PatternError) as context:
            generate_codes(5, (2,), "AB")
        self.assertEqual(context.exception.key, "core_capacity")
        self.assertEqual(context.exception.details, {"capacity": 4})


class AnalysisTests(unittest.TestCase):
    def test_original_samples(self):
        analysis = analyze_codes("\n".join(SAMPLE_CODES))
        self.assertEqual(analysis.block_lengths, (5, 5, 5, 5))
        self.assertEqual(analysis.count, 7)
        self.assertEqual(analysis.duplicates, 0)
        self.assertEqual(analysis.total_length, 20)
        self.assertEqual(analysis.common_prefix, "")
        self.assertEqual(analysis.position_template, "?????-?????-?????-?????")
        observed = set("".join(SAMPLE_CODES).replace("-", ""))
        self.assertEqual(set(analysis.alphabet), observed)
        self.assertTrue(observed <= set(DEFAULT_ALPHABET))
        self.assertEqual(sum(analysis.character_frequencies.values()), 140)
        self.assertEqual(analysis.character_frequencies["3"], 8)

    def test_normalization_and_duplicates(self):
        analysis = analyze_codes("  ab-12  \n\nAB-13\nab-12\n")
        self.assertEqual(analysis.position_template, "AB-1?")
        self.assertEqual(analysis.common_prefix, "AB1")
        self.assertEqual(analysis.count, 3)
        self.assertEqual(analysis.duplicates, 1)
        self.assertEqual(analysis.character_frequencies["A"], 3)

    def test_single_sample_is_observation(self):
        analysis = analyze_codes("AB-12")
        self.assertEqual(analysis.position_template, "AB-12")
        self.assertEqual(analysis.common_prefix, "AB12")

    def test_invalid_samples(self):
        for value in (None, "", " \n ", "AB--12", "-AB", "AB-", "AB CD",
                      "AB_12", "ÁB-12", "ß-12", "AB-12\nA-12",
                      "A" * 33, "-".join(["A"] * 33),
                      "-".join(["A" * 32] * 7)):
            with self.subTest(value=value), self.assertRaises(ValueError):
                analyze_codes(value)

    def test_input_size_limits(self):
        with self.assertRaisesRegex(ValueError, "1 MB"):
            analyze_codes(" " * 1_048_577)
        with self.assertRaisesRegex(ValueError, "1 MB"):
            analyze_codes("é" * 524_289)
        with self.assertRaisesRegex(ValueError, "10000 líneas"):
            analyze_codes("A\n" * 10_001)
        self.assertEqual(analyze_codes("A\n" * 10_000).count, 10_000)


class GenerationTests(unittest.TestCase):
    def test_default_format_and_uniqueness(self):
        codes = generate_codes(500)
        self.assertEqual(len(codes), 500)
        self.assertEqual(len(set(codes)), 500)
        for code in codes:
            self.assertEqual(tuple(map(len, code.split("-"))), (5, 5, 5, 5))
            self.assertTrue(set(code.replace("-", "")) <= set(DEFAULT_ALPHABET))

    def test_prefix_crosses_block_separator(self):
        codes = generate_codes(2, (2, 2), "AB", "ABA")
        self.assertTrue(all(code.replace("-", "").startswith("ABA") for code in codes))

    def test_full_capacity(self):
        self.assertEqual(set(generate_codes(4, (2,), "AB")), {"AA", "AB", "BA", "BB"})
        self.assertEqual(set(generate_codes(2, (2, 2), "AB", "ABA")), {"AB-AA", "AB-AB"})
        self.assertEqual(generate_codes(1, (2, 2), "AB", "ABBA"), ["AB-BA"])
        self.assertEqual(generate_codes(1, (3,), "A"), ["AAA"])

    def test_sampling_terminates_without_retry_even_with_constant_random(self):
        for selector in (lambda remaining: 0, lambda remaining: remaining - 1):
            with patch("kiskas_core.secrets.randbelow", side_effect=selector) as random:
                codes = generate_codes(16, (4,), "AB")
                self.assertEqual(len(set(codes)), 16)
                self.assertEqual(random.call_count, 16)

    def test_capacity_exceeded(self):
        for arguments in ((5, (2,), "AB", ""), (3, (2, 2), "AB", "ABA"),
                          (2, (2,), "AB", "AB"), (2, (3,), "A", "")):
            with self.subTest(arguments=arguments), self.assertRaisesRegex(ValueError, "únicas"):
                generate_codes(*arguments)

    def test_invalid_options(self):
        for count in (None, False, 0, -1, 10_001, 1.5, "2"):
            with self.subTest(count=count), self.assertRaises(ValueError):
                generate_codes(count)
        for blocks in (None, [5, 5], (), (0,), (33,), (True,), (1.5,),
                       (1,) * 33, (32,) * 7):
            with self.subTest(blocks=blocks), self.assertRaises(ValueError):
                generate_codes(1, blocks)
        for alphabet in (None, "", "AA", "ab", "A-B", "A B", "Á", "A_"):
            with self.subTest(alphabet=alphabet), self.assertRaises(ValueError):
                generate_codes(1, (2,), alphabet)
        for prefix in (None, "C", "a", "A-B", "AAA"):
            with self.subTest(prefix=prefix), self.assertRaises(ValueError):
                generate_codes(1, (2,), "AB", prefix)

    def test_maximum_generation_and_length(self):
        self.assertEqual(len(set(generate_codes(10_000, (14,), "AB"))), 10_000)
        code = generate_codes(1, (32,) * 6 + (8,), "A")[0]
        self.assertEqual(len(code.replace("-", "")), 200)


if __name__ == "__main__":
    unittest.main()
