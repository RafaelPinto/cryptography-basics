import re
from collections import Counter
from pathlib import Path


def letters_in_file(filepath: Path):
    with open(filepath, "r") as fhandle:
        for line in fhandle:
            yield from [letter.lower() for letter in re.findall(r"\w", line)]


def letters_count(filepath: Path):
    return Counter(letters_in_file(filepath))
