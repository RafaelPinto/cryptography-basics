import re
from collections import Counter
from pathlib import Path
import string
from typing import Dict

import matplotlib.pyplot as plt

from pypdf import PdfReader


def letters_in_file(filepath: Path):
    with open(filepath, "r") as fhandle:
        for line in fhandle:
            yield from [letter.lower() for letter in re.findall(r"\w", line)]


def letters_count(filepath: Path):
    return Counter(letters_in_file(filepath))


def count_pdf_file_letters(
        pdf_filepath: Path,
        page_start: int,
        page_stop: int,
        y_min: int,
        y_max=int
        ) -> Counter:

    reader = PdfReader(pdf_filepath)
    counter = Counter()

    def visitor_body(text, cm, tm, font_dict, font_size):
        y = tm[5]
        if y > y_min and y < y_max:
            if text.strip() != "":
                counter.update(
                    [letter.lower() for letter in re.findall(r"\w", text)]
                )

    for page_number in range(page_start, page_stop, 1):
        page = reader.pages[page_number]
        page.extract_text(visitor_text=visitor_body)
    return counter


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


def main():
    independence_file = Path("declaration-transcript.txt")
    independence_rot13_file = Path("independence_rot13.txt")
    caesar_cipher(
        clear_text_path=independence_file,
        rot=13,
        output_path=independence_rot13_file,
    )
    independence_letter_count = letters_count(independence_rot13_file)

    independence_letter_count_sorted = {
        letter: independence_letter_count[letter]
        for letter in string.ascii_lowercase
    }

    fig, axs = plt.subplots(1, 1, figsize=(9, 3))
    axs.bar(
        list(independence_letter_count_sorted.keys()),
        list(independence_letter_count_sorted.values()),
    )
    fig.suptitle('Encryted Independence Declaration letter count')
    plt.show()


if __name__ == "__main__":
    main()
