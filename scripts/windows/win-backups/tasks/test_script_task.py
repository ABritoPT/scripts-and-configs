import pytest
import subprocess
from os import path
import time
from script_task import Script

def test_fake_folder():
    sc = Script("fake folder test", "dir", "ZZZ:\\fake\\folder")
    with pytest.raises(ValueError, match="Start in folder does not exist"):
        sc.run()

@pytest.fixture
def empty_test_file():
    test_file_name = "test_script_" + str(time.time_ns())
    test_file_path = path.abspath(path.join(path.dirname(path.realpath(__file__)),
                                  path.pardir ,"tests", test_file_name))
    res = subprocess.call("copy /b NUL " + test_file_path, shell=True)
    assert res==0, "setup successful"
    
    yield test_file_path

    res = subprocess.call("del "+test_file_path, shell=True)
    assert path.exists(test_file_path) == False, "teardown successful"

def test_dry_run(empty_test_file):
    sc = Script("dry-run test delete file", "del "+empty_test_file)
    sc.run(True)
    assert path.exists(empty_test_file) == True

def test_real_run(empty_test_file):
    sc = Script("real-run test delete file", "del "+empty_test_file)
    sc.run(False)
    assert path.exists(empty_test_file) == False

def test_correct_command():
    sc = Script("test correct cmd", "dir")
    res = sc.run(False)
    assert res == 0

def test_wrong_command():
    sc = Script("test wrong cmd", "dirrrrrr")
    res = sc.run(False)
    assert res == 1