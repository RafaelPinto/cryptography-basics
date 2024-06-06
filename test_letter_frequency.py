import string
import tempfile
import unittest
from pathlib import Path

from letters_frequency import letters_count, letters_in_file

TEST_TEXT = """
Mr. Jock, TV quiz PhD, bags few lynx.
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
