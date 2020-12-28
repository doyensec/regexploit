import pytest

from regexploit.ast.at import EndOfString
from regexploit.ast.sre import SreOpParser


def from_regex(pattern: str):
    return SreOpParser().parse_sre(pattern)


@pytest.mark.parametrize(
    "r",
    [
        r".*b*",
        r".*\w*b*",
        r".+b*",
    ],
)
def test_cannot_backtrack(r):
    dollar = EndOfString()
    dollar.set_character(from_regex(r).elements)
    assert dollar.character.is_any


@pytest.mark.parametrize(
    "r",
    [
        r"x[ab]*b*",
        r"x+[ab]*",
        r"x+a*[ab]*a*b*",
    ],
)
def test_dollar_simple(r):
    dollar = EndOfString()
    dollar.set_character(from_regex(r).elements)
    assert dollar.character == from_regex("[ab]")


@pytest.mark.parametrize(
    "r",
    [
        r"\w*b*",
        r"x\w*\w*b*",
        r"\w+b*",
    ],
)
def test_dollar_optionals_contained_by_mandatory(r):
    dollar = EndOfString()
    dollar.set_character(from_regex(r).elements)
    assert dollar.character == from_regex(r"[\w]").expand_categories()


def test_whole_string():
    dollar = EndOfString()
    dollar.set_character(from_regex(r"a*a*").elements)
    assert dollar.character == from_regex(r"[a]")


def test_real():
    dollar = EndOfString()
    dollar.set_character(from_regex(r"-\d+(\s*\s*\s*)").elements)
    assert dollar.character == from_regex(r"[\s]")
