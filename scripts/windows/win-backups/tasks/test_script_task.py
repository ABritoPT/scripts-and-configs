import pytest
from os import path
from .script_task import ScriptTask

def test_fake_folder():
    sc = ScriptTask("fake folder test", {}, "dir", "ZZZ:\\fake\\folder")
    with pytest.raises(ValueError, match="Start in folder does not exist"):
        sc.run()

def test_paths_setup():
    paths_map = { 'DRIVE': 'R', 'FILE': 'abc.def' }
    st = ScriptTask("test paths setup", paths_map, "$DRIVE$:\\$FILE$", "$DRIVE$:\\")
    assert st.target == "R:\\abc.def"
    assert st.start_in == "R:\\"

def test_dry_run(empty_test_file):
    sc = ScriptTask("dry-run test delete file", {}, "del "+empty_test_file)
    sc.run(True)
    assert path.exists(empty_test_file) == True

def test_real_run(empty_test_file):
    sc = ScriptTask("real-run test delete file", {}, "del "+empty_test_file)
    sc.run(False)
    assert path.exists(empty_test_file) == False

def test_correct_command():
    sc = ScriptTask("test correct cmd", {}, "dir")
    res = sc.run(False)
    assert res == 0

def test_wrong_command():
    sc = ScriptTask("test wrong cmd", {}, "dirrrrrr")
    res = sc.run(False)
    assert res == 1