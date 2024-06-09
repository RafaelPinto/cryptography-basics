import re
from collections import Counter
from pathlib import Path
import string
from typing import Dict


def letters_in_file(filepath: Path):
    with open(filepath, "r") as fhandle:
        for line in fhandle:
            yield from [letter.lower() for letter in re.findall(r"\w", line)]


def letters_count(filepath: Path):
    return Counter(letters_in_file(filepath))


def build_substitution_table(
        rot: int,
        reversed: bool = False
        ) -> Dict[int, int]:
    """Build letter substitution mapping between the alphabet letters
    (clear text) and those rotated `rot` times (encrypted text).

    If reversed is True, the result will map the encrypted text letters
    to the clear text letters. This is useful in decrytion.
    """
    alphabet = string.ascii_lowercase
    rot = rot % len(alphabet)
    alphabet_rot = alphabet[rot:] + alphabet[:rot]
    rotation_letters = [
        alphabet + alphabet.upper(),
        alphabet_rot + alphabet_rot.upper(),
    ]
    if reversed:
        rotation_letters.reverse()
    return str.maketrans(*rotation_letters)


def rotate_text(text: str, substitution_table: Dict[int, int]) -> str:
    """
    Substitute the letters in the `text` using the mapping given
    in the substitution table.
    """
    return text.translate(substitution_table)


def caesar_cipher(clear_text_path: Path, rot: int, output_path: Path):
    """
    Substitute the letters in the `clear_path_text` by those after
    rotating the alphabet `rot` times. Write the output to the given
    `output_path`.
    """
    trans_table = build_substitution_table(rot=rot)
    with (
        open(clear_text_path, 'r') as reader,
        open(output_path, 'w') as writer
    ):
        for line in reader:
            writer.write(rotate_text(
                text=line,
                substitution_table=trans_table)
            )

