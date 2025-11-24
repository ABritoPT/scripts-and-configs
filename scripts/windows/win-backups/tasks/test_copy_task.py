import pytest
import re
import subprocess
from os import path
import time
from copy_task import Copy

def get_tests_dir():
    return path.abspath(path.join(path.dirname(path.realpath(__file__)),
                                  path.pardir ,"tests"))

@pytest.fixture
def empty_test_file():
    test_file_name = "test_script_" + str(time.time_ns())
    test_file_path = path.join(get_tests_dir(), test_file_name)
    res = subprocess.call("copy /b NUL " + test_file_path, shell=True)
    assert res==0, "setup successful"
    
    yield test_file_path

    res = subprocess.call("del " + test_file_path, shell=True)
    assert path.exists(test_file_path) == False, "teardown successful"

def cars_directory_contents():
    return {
        'subaru': {
            '?files': [ 'BRZ.txt', 'WRX.txt', 'Impreza.txt' ]
        },
        'peugeot': {
            '205': {
                '?files': [ '205-gti.txt', '205-xs.txt' ]
            },
            '106': {
                '?files': [ '106-xs.txt', '106-grd.txt' ]
            },
            '?files': ['RCZ.txt']
        }
    }

def __process_dir(dir_name, dir_contents, parent_dir):
    curr_dir = path.join(parent_dir, dir_name)
    outcome = subprocess.call("md " + curr_dir, shell=True)

    for k,v in dir_contents.items():
        if k == '?files':
            for f in v:
                f_path = path.join(curr_dir, f)
                res = subprocess.call("copy /b NUL " + f_path, shell=True)
                outcome = max(res,outcome)
        else:
            res = __process_dir(k, v, curr_dir)
            outcome = max(res,outcome)
    return outcome

def __recurse_delete_dir(path):
    subprocess.call("rd /s /q " + path, shell=True)

@pytest.fixture
def cars_directory_structure():
    contents = cars_directory_contents()
    tests_dir = get_tests_dir()
    car_tests_dir = path.join(tests_dir, "cars_test")
    res = __process_dir("cars_test", contents, tests_dir)
    assert res==0, "setup successful"

    yield car_tests_dir

    res = __recurse_delete_dir(car_tests_dir)
    assert path.exists(car_tests_dir) == False, "teardown successful"

def test_fake_source():
    dir = "ZZZ:\\fake\\folder"
    ct = Copy("fake source test", dir, dir)
    with pytest.raises(ValueError, match=re.escape("Path does not exist: " + dir)):
        ct.run()

def test_dry_run(empty_test_file):
    dst = empty_test_file + ".cpy"
    ct = Copy("dry-run test copy file", empty_test_file, dst)
    ct.run(True)
    assert path.exists(dst) == False

def test_real_run(empty_test_file):
    dst = empty_test_file + ".cpy"
    ct = Copy("dry-run test copy file", empty_test_file, dst)
    ct.run(False)
    assert path.exists(dst) == True
    subprocess.call("del " + dst, shell=True)

def test_complex_copy(cars_directory_structure):
    src = cars_directory_structure
    dst = src + "-copy"
    ct = Copy("complex copy test", src, dst)
    
    ct.run(False)
    assert path.exists(path.join(dst, "subaru", "BRZ.txt")) == True
    assert path.exists(path.join(dst, "peugeot", "205", "205-xs.txt")) == True
    assert path.exists(path.join(dst, "peugeot", "106", "106-grd.txt")) == True
    assert path.exists(path.join(dst, "peugeot", "RCZ.txt")) == True
    
    __recurse_delete_dir(dst)
