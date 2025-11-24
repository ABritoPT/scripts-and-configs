import pytest
import subprocess
import os
import time
from script import Script

def test_fake_folder():
    sc = Script("fake folder test", "dir", "ZZ:\\fake\\folder")
    with pytest.raises(ValueError, match="Start in folder does not exist"):
        sc.run()

@pytest.fixture
def empty_test_file():
    test_file_name = "test_script_" + str(time.time_ns())
    test_file_path = os.path.dirname(os.path.realpath(__file__)) + "\\..\\tests\\" + test_file_name
    res = subprocess.call("copy /b NUL " + test_file_path, shell=True)
    assert res==0, "setup successful"
    
    yield test_file_path

    res = subprocess.call("del "+test_file_path, shell=True)
    assert os.path.exists(test_file_path) == False, "teardown successful"

def test_dry_run(empty_test_file):
    sc = Script("dry-run test delete file", "del "+empty_test_file)
    sc.run(True)
    assert os.path.exists(empty_test_file) == True

def test_real_run(empty_test_file):
    sc = Script("real-run test delete file", "del "+empty_test_file)
    sc.run(False)
    assert os.path.exists(empty_test_file) == False

def test_correct_command():
    sc = Script("test correct cmd", "dir")
    res = sc.run(False)
    assert res == 0

def test_wrong_command():
    sc = Script("test wrong cmd", "dirrrrrr")
    res = sc.run(False)
    assert res == 1