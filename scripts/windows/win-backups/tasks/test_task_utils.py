import pytest
import re
from . import task_utils

def test_simple_replace():
    key = {
        "ABC": "123",
        "DEF": "456",
        "GHI": "789"
    }
    test_str = "$ABC$ABC$DEF$$GHI$"
    res = task_utils.resolve_placeholders(test_str, key)
    assert res == "123ABC456789"

def test_iterative_replace():
    key = {
        "ABC": "$DEF$",
        "DEF": "$GHI$",
        "GHI": "789"
    }
    test_str = "$ABC$ABC$DEF$$GHI$"
    res = task_utils.resolve_placeholders(test_str, key)
    assert res == "789ABC789789"

def test_no_replace():
    key = { "ABC": "123" }
    test_str = "ABCDEF"
    res = task_utils.resolve_placeholders(test_str, key)
    assert res == test_str

def test_unpaired_placeholder():
    key = { "ABC": "123" }
    test_str = "$ABC$$ABCDEF"
    res = task_utils.resolve_placeholders(test_str, key)
    assert res == "123$ABCDEF"

def test_missing_mapping():
    key = { "ABC": "123" }
    test_str = "$ABC$$DEF$"
    with pytest.raises(KeyError, match=re.escape("No mapping for placeholder $DEF$")):
        res = task_utils.resolve_placeholders(test_str, key)