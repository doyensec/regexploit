import re
from json import dumps
from unittest.mock import Mock

import pytest

from regexploit.bin.regexploit_js import handle_line_from_node
from regexploit.languages.javascript import fix_js_regex


@pytest.mark.parametrize(
    "r,f",
    [
        # Carat
        (r"[^]", r"\^"),
        (r"[^][^][^]", r"\^\^\^"),
        (r"([^])+([^])+([^])+", r"(\^)+(\^)+(\^)+"),
        (r"[^][^][^]([\[^])+", r"\^\^\^([\[^])+"),
        # Named groups
        (r"(?<x>y>)+(?<ab_cD0>abc)\(?<a>", r"(?P<x>y>)+(?P<ab_cD0>abc)\(?<a>"),
        # Hyphen in character class
        (r"[\w-:]", r"[\w\-:]"),
        (r"[!-\w]", r"[!\-\w]"),
    ],
)
def test_fixes(r, f):
    with pytest.raises(re.error):
        re.compile(r)
    fixed = fix_js_regex(r)
    assert fixed == f
    re.compile(fixed)


@pytest.mark.parametrize(
    "pat,next_called,recorded",
    [
        ("ab*cdef", False, False),  # too few stars
        ("ab+c+def", True, False),
        ("ab*b+b*c", True, True),
        ("a[^](?<xyz>c*)*d", True, True),
        ("a[^](?<xyz>c*)d*", True, False),
    ],
)
def test_handle_line_from_node(pat, next_called, recorded):
    output = Mock(spec=["next", "record"])
    line_json = dict(pattern=pat, lineno=1, filename="testfile")
    handle_line_from_node(dumps(line_json), output)
    if next_called:
        output.next.assert_called_once()
    else:
        output.next.assert_not_called()
    if recorded:
        output.record.assert_called_once()
    else:
        output.record.assert_not_called()
