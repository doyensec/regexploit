import re
from unittest.mock import Mock

from regexploit.bin.regexploit_csharp import handle_file
from regexploit.languages.csharp_string_extractor import find_regexes


def test_csharp():
    with open("tests/test.cs", "rb") as f:
        code = f.read()
    found = list(find_regexes(code))
    assert len(found) == 6
    assert found[0].pattern == "Not a regex*****"
    assert found[1].pattern == '\\w+_[\\w"]+_\\w+w'
    assert found[2].pattern == r'x"\d+.\d+.\d+!'
    assert found[2].lineno == 15
    assert not found[2].definitely_regex
    assert found[3].definitely_regex
    assert found[4].flags == re.I
    assert found[5].flags == re.X


def test_handle_file():
    output = Mock(spec=["next", "record"])
    handle_file("tests/test.cs", output)
    assert output.next.call_count == 5
    assert output.record.call_count == 3
