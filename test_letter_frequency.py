from collections import Counter
import string
import tempfile
import unittest
from pathlib import Path

from letters_frequency import (
    build_substitution_table,
    caesar_cipher,
    letters_count,
    letters_in_file,
    rotate_text,
)

TEST_TEXT = """Mr. Jock, TV quiz PhD, bags few lynx.
Mr. Jock, TV quiz PhD, bags few lynx.
"""


class TestFileParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmpdir = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmpdir.cleanup)
        cls.test_text_path = Path(cls.tmpdir.name) / "test_text.txt"

        with open(cls.test_text_path, "w+") as fhandle:
            fhandle.write(TEST_TEXT)

    def test_letters_in_file_two_lines(self):
        self.assertEqual(
            list(letters_in_file(self.test_text_path)),
            "m r j o c k t v q u i z p h d b a g s f e w l y n x".split() * 2,
        )

    def test_letter_count(self):
        count = letters_count(self.test_text_path)

        self.assertEqual(
            count,
            {letter: 2 for letter in string.ascii_lowercase}
        )


class TestPDFParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_pdf_path = Path("sample-pdf.pdf")

    def test_count_pdf_file_letters_wo_header_and_footer(self):
        expected_text = """
            This is the first paragraph on the first page.
            This is the second paragraph on the first page.
            This is the second paragraph on the second page.
            This is the second paragraph on the second page.
        """
        expected_letter_count = Counter(
            [
                char.lower()
                for char in expected_text
                if char.lower() in string.ascii_lowercase
            ]
        )

        self.assertEqual(
            count_pdf_file_letters(
                self.test_pdf_path,
                page_start=0,
                page_stop=2,
                y_min=50,
                y_max=760,
            ),
            expected_letter_count,
        )


class TestCaesarCipher(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmpdir = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmpdir.cleanup)
        cls.test_text_path = Path(cls.tmpdir.name) / "test_text.txt"

        with open(cls.test_text_path, "w+") as fhandle:
            fhandle.write(TEST_TEXT)

    def test_rot13(self):
        encrypted_text_path = Path(self.tmpdir.name) / "encrypted_text.txt"

        caesar_cipher(
            clear_text_path=self.test_text_path,
            rot=13,
            output_path=encrypted_text_path,
        )

        with open(encrypted_text_path, "r") as fhandle:
            encrypted_text = "".join(fhandle.readlines())

        self.assertEqual(
            encrypted_text,
            "Ze. Wbpx, GI dhvm CuQ, ontf srj ylak.\n"
            "Ze. Wbpx, GI dhvm CuQ, ontf srj ylak.\n"
        )

    def test_rotate_text_same_text_with_rot_zero(self):
        trans_table = build_substitution_table(rot=0)
        self.assertEqual(
            rotate_text(text=TEST_TEXT, substitution_table=trans_table),
            TEST_TEXT,
        )

    def test_rotate_text_negative_rotation(self):
        input_text = "abcd"
        expected_output_text = "xyza"
        trans_table = build_substitution_table(rot=-3)
        self.assertEqual(
            rotate_text(text=input_text, substitution_table=trans_table),
            expected_output_text,
        )

    def test_rotate_text_with_rot_lt_alphabet_character_count(self):
        input_text = "abcd"
        expected_output_text = "xyza"
        trans_table = build_substitution_table(rot=49)
        self.assertEqual(
            rotate_text(text=input_text, substitution_table=trans_table),
            expected_output_text,
        )

    def test_rotate_text_for_decryption(self):
        input_text = "xyza"
        expected_output_text = "abcd"
        trans_table = build_substitution_table(rot=49, reversed=True)
        self.assertEqual(
            rotate_text(text=input_text, substitution_table=trans_table),
            expected_output_text,
        )
