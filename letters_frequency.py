import re
from collections import Counter
from pathlib import Path
import string


def letters_in_file(filepath: Path):
    with open(filepath, "r") as fhandle:
        for line in fhandle:
            yield from [letter.lower() for letter in re.findall(r"\w", line)]


def letters_count(filepath: Path):
    return Counter(letters_in_file(filepath))


def rotate_text(text: str, rot: int) -> str:
    """
    Substitute the letters in the `text` by those after
    rotating the alphabet `rot` times.
    """
    alphabet = string.ascii_lowercase
    rot = rot % len(alphabet)
    alphabet_rot = alphabet[rot:] + alphabet[:rot]
    trans_table = str.maketrans(
        alphabet + alphabet.upper(),
        alphabet_rot + alphabet_rot.upper(),
    )
    return text.translate(trans_table)


def caesar_cipher(clear_text_path: Path, rot: int, output_path: Path):
    """
    Substitute the letters in the `clear_path_text` by those after
    rotating the alphabet `rot` times. Write the output to the given
    `output_path`.
    """
    with (
        open(clear_text_path, 'r') as reader,
        open(output_path, 'w') as writer
    ):
        for line in reader:
            writer.write(rotate_text(text=line, rot=rot))

