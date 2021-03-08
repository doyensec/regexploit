import ast
import re
import textwrap
from unittest.mock import Mock

from regexploit.bin.regexploit_python_ast import handle_file
from regexploit.found_regex import FoundRegex
from regexploit.languages.python_node_visitor import PythonNodeVisitor


def patterns_from_code(code: str):
    pnv = PythonNodeVisitor()
    code = textwrap.dedent(code)
    pnv.visit(ast.parse(code))
    return pnv.patterns


def test_basic():
    code = """
    MY_RE = "abc+d+"
    def x():
        '''Just*a*docstring*'''
        a = "nostarsorpluses"
        b = "(" + re.sub("aregex", "*****", "notaregex", flags=re.A) + ")"
        return re.compile(b"x*y*z", re.X | re.MULTILINE)
    """
    patterns = patterns_from_code(code)
    assert len(patterns) == 3
    assert patterns[0] == FoundRegex(2, "abc+d+", 0, False)
    assert patterns[1] == FoundRegex(6, "aregex", re.A, True)
    assert patterns[2] == FoundRegex(7, "x*y*z", re.X | re.MULTILINE, True)


def test_file():
    output = Mock(spec=["next"])
    handle_file(__file__, output)
    assert output.next.call_count == 2  # abc+d+, x*y*z, code string errors
