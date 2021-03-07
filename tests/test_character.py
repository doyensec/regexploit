import pytest
from sre_parse import parse as sre_parse

from regexploit.ast.categories import Category
from regexploit.ast.char import Character
from regexploit.ast.sre import SreOpParser


def from_regex(pattern: str) -> Character:
    (parsed_char,) = sre_parse(pattern)
    char = SreOpParser().parse_op(*parsed_char)
    assert isinstance(char, Character)
    return char


def test_literal_and():
    assert from_regex("[abc]") & from_regex("[bcd]") == from_regex("[bc]")


def test_literal_negated_and():
    assert from_regex("[^abc]") & from_regex("[^bcd]") == from_regex("[^a-d]")


def test_literal_mixed_and():
    assert from_regex("[abcz]") & from_regex("[^bcd]") == from_regex("[az]")
    assert from_regex("[^bcd]") & from_regex("[abcz]") == from_regex("[az]")


def test_category_and():
    assert from_regex(r"[\s\d]") & from_regex(r"[\d\w]") == from_regex(r"\d")


def test_category_negated_and():
    assert from_regex(r"[^\s\d]") & from_regex(r"[^\d\w]") == from_regex(r"[^\s\d\w]")


def test_category_negated_and_simplifies_to_nothing():
    assert (from_regex(r"[^\s\d]") & from_regex(r"[^\D]")) is None


def test_mixed_and():
    assert from_regex(r"[abc123\s]") & from_regex(r"[^\d\s]") == from_regex("[abc]")


def test_mixed_and_none():
    c = from_regex(r"[123]") & from_regex(r"[^\d\s]")
    assert c is None


@pytest.mark.parametrize(
    "r",
    [
        r"a",
        r"\s",
        r"[a\s\S\d]",
        r"[A-z]",
        r"[^A-z\d]",
    ],
)
def test_and_any_none(r):
    any = Character.ANY()
    other = from_regex(r)
    assert (any & other) == other
    assert (other & any) == other
    assert (any & None) is None
    assert (None & any) is None


def test_class():
    assert from_regex("[abc]").exact_character_class() == from_regex("[cba]")


def test_negate_simple():
    assert from_regex("a").negate() == from_regex("[^a]")
    assert from_regex(r"\w").negate() == from_regex(r"[^\w]")
    assert from_regex("[^ab]").negate() == from_regex("[ab]")
    assert from_regex(r"[^\s]").negate() == from_regex(r"\s")


def test_negate_mixed():
    assert from_regex(r"[a\s\w]").negate() == from_regex(r"[^a\s\w]")


def test_or():
    assert from_regex("a") | from_regex("a") == from_regex("a")
    assert from_regex("a") | from_regex("b") == from_regex("[ab]")
    assert from_regex(r"\w") | from_regex("b") == from_regex(r"\w").expand_categories()
    assert (
        from_regex(r"\w") | from_regex("9") == from_regex(r"[9\w]").expand_categories()
    )
    assert from_regex("[^a]") | from_regex("[^b]") == from_regex(".")


def test_category_category_covers_all():
    assert from_regex(r"[\s\S]").is_any is True
    assert from_regex(r"[\Dd\d]").is_any is True


def test_negative_lookahead():
    assert SreOpParser().parse_sre(r"(?![0248])(?!6)(?!a)(?!xyz123)\d") == from_regex(
        r"[13579]"
    )


def test_category_category_covers_none():
    assert SreOpParser().parse_sre(r"[^x0-9\w\W]") is None


@pytest.mark.parametrize(
    "category_identifier,category_enum,character",
    [
        ("w", Category.WORD, "b"),
        ("w", Category.WORD, "C"),
        ("w", Category.WORD, "_"),
        ("w", Category.WORD, "3"),
        ("W", Category.NOT_WORD, "-"),
        ("W", Category.NOT_WORD, "."),
        ("s", Category.SPACE, "\xa0"),
        ("s", Category.SPACE, "\v"),
    ],
)
def test_categories(category_identifier: str, category_enum: Category, character: str):
    # \w ~= [a-zA-Z0-9_], \s ~= [ \t\n\r\f\v]
    category_characters = from_regex("\\" + category_identifier).expand_categories()
    char = Character.LITERAL(ord(character))
    assert category_characters | char == category_characters
    assert category_characters & char == char
    assert category_enum.contains(ord(character))


@pytest.mark.parametrize(
    "category_identifier,category_enum,not_character",
    [
        ("w", Category.WORD, "-"),
        ("W", Category.NOT_WORD, "_"),
        ("W", Category.NOT_WORD, "9"),
        ("s", Category.SPACE, "\x00"),
        ("S", Category.NOT_SPACE, "\f"),
    ],
)
def test_not_categories(
    category_identifier: str, category_enum: Category, not_character: str
):
    category_characters = from_regex("\\" + category_identifier).expand_categories()
    char = Character.LITERAL(ord(not_character))
    assert category_characters & char is None
    assert not category_enum.contains(ord(not_character))
