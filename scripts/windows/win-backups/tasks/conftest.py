import pytest
from os import path
import time
import subprocess

def get_tests_dir(file_ref=__file__):
    return path.abspath(path.join(path.dirname(path.realpath(file_ref)),
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

def process_dir(dir_name, dir_contents, parent_dir):
    curr_dir = path.join(parent_dir, dir_name)
    outcome = subprocess.call("md \"" + curr_dir + "\"", shell=True)

    for k,v in dir_contents.items():
        if k == '?files':
            for f in v:
                f_path = path.join(curr_dir, f)
                res = subprocess.call("copy /b NUL \"" + f_path + "\"", shell=True)
                outcome = max(res,outcome)
        else:
            res = process_dir(k, v, curr_dir)
            outcome = max(res,outcome)
    return outcome

def recurse_delete_dir(path):
    subprocess.call("rd /s /q \"" + path + "\"", shell=True)

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

@pytest.fixture
def cars_directory_structure():
    contents = cars_directory_contents()
    tests_dir = get_tests_dir()
    car_tests_dir = path.join(tests_dir, "cars_test")
    res = process_dir("cars_test", contents, tests_dir)
    assert res==0, "setup successful"

    yield car_tests_dir

    res = recurse_delete_dir(car_tests_dir)
    assert path.exists(car_tests_dir) == False, "teardown successful"

def tv_shows_directory_contents():
    return {
        'Seinfeld': {
            'Season 1': {
                '?files': [ 'S01E01.mp4', 'S01E02.mp4', 'S01E03.mp4' ]
            },
            'Season 2': {
                '?files': [ 'S02E01.mp4', 'S02E02.mp4', 'S02E03.mp4' ]
            },
            'Season 3': {
                '?files': [ 'S03E01.mp4', 'S03E02.mp4', 'S03E03.mp4' ]
            },
            '?files': [ 'seinfeld.nfo' ]
        },
        'Curb Your Enthusiasm': {
            'Season 1': {
                '?files': [
                    'S01E01.mp4', 'S01E02.mp4', 'S01E03.mp4',
                    'S01E01.srt', 'S01E02.srt', 'S01E03.srt'
                ]
            },
            'Season 2': {
                '?files': [ 'S02E01.mp4', 'S02E02.mp4', 'S02E03.mp4' ]
            },
            'Season 3': {
                '?files': [ 'S03E01.mp4', 'S03E02.mp4', 'S03E03.mp4' ]
            },
            '?files': [ 'rip.nfo' ]
        }
    }

@pytest.fixture
def tv_shows_directory_structure():
    contents = tv_shows_directory_contents()
    tests_dir = get_tests_dir()
    shows_tests_dir = path.join(tests_dir, "TV Shows")
    res = process_dir("TV Shows", contents, tests_dir)
    assert res==0, "setup successful"

    yield shows_tests_dir

    res = recurse_delete_dir(shows_tests_dir)
    assert path.exists(shows_tests_dir) == False, "teardown successful"