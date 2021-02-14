import sys
import unicodedata
from enum import Enum, auto
from typing import Set


class Category(Enum):
    DIGIT = auto()
    NOT_DIGIT = auto()
    WORD = auto()
    NOT_WORD = auto()
    SPACE = auto()
    NOT_SPACE = auto()

    @property
    def is_positive(self) -> bool:
        return not self.name.startswith("NOT_")

    def negate(self) -> "Category":
        if self.is_positive:
            return Category[f"NOT_{self.name}"]
        else:
            return Category[self.name[4:]]

    def example(self) -> str:
        return EXAMPLE_FOR_CAT[self]

    def contains(self, literal: int) -> bool:
        c = chr(literal)
        unicat = unicodedata.category(c)
        if self is Category.DIGIT:
            return unicat == "Nd"
        if self is Category.NOT_DIGIT:
            return unicat != "Nd"
        if self is Category.WORD:
            return (
                unicat[0] == "L" or unicat == "Nd" or literal == 0x5F
            )  # underscore is a word character
        if self is Category.NOT_WORD:
            return unicat[0] != "L" and unicat != "Nd" and literal != 0x5F
        if self is Category.SPACE:
            return unicat == "Zs" or c in (" ", "\n", "\t", "\r", "\f", "\v")
        if self is Category.NOT_SPACE:
            return unicat != "Zs" and c not in (" ", "\n", "\t", "\r", "\f", "\v")


CATS = {}


def list_category(category, full_unicode: bool = False):
    if (cached := CATS.get(category)) :
        yield from cached
    for data in range((sys.maxunicode + 1) if full_unicode else 256):
        c = chr(data)
        unicat = unicodedata.category(c)
        if category is Category.DIGIT:
            if unicat == "Nd":
                yield data
        elif category is Category.NOT_DIGIT:
            if unicat != "Nd":
                yield data
        elif category is Category.WORD:
            if unicat[0] == "L" or unicat == "Nd" or data == 0x5F:
                yield data
        elif category is Category.NOT_WORD:
            if unicat[0] != "L" and unicat != "Nd" and data != 0x5F:
                yield data
        elif category is Category.SPACE:
            if unicat == "Zs" or c in (" ", "\n", "\t", "\r", "\f", "\v"):
                yield data
        elif category is Category.NOT_SPACE:
            if unicat != "Zs" and c not in (" ", "\n", "\t", "\r", "\f", "\v"):
                yield data


def covers_any(categories: Set[Category]) -> bool:
    for c in categories:
        if c.is_positive and c.negate() in categories:
            return True
    return False


# CATS[sre_parse.CATEGORY_DIGIT] = list(list_category(sre_parse.CATEGORY_DIGIT))
# CATS[sre_parse.CATEGORY_SPACE] = list(list_category(sre_parse.CATEGORY_SPACE))
# CATS[sre_parse.CATEGORY_WORD] = list(list_category(sre_parse.CATEGORY_WORD))
EXAMPLE_FOR_CAT = {
    Category.DIGIT: "4",
    Category.NOT_DIGIT: "!",
    Category.WORD: "w",
    Category.NOT_WORD: "$",
    Category.SPACE: " ",
    Category.NOT_SPACE: ".",
}
