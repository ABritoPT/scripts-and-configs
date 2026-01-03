import pytest
import re
import subprocess
from os import path
from os import stat
from .archive_task import ArchiveTask
from . import conftest

def test_fake_source():
    dir = "ZZZ:\\fake\\folder"
    at = ArchiveTask("fake source test", {}, dir, dir, "a.zip")
    with pytest.raises(ValueError, match=re.escape("Path does not exist: " + dir)):
        at.run()

def test_paths_setup():
    dir = "$DRIVE$:\\"
    paths_map = { 'DRIVE': 'R', 'FILE1': 'abc.def' }
    at = ArchiveTask("test paths setup", paths_map, dir, [dir,dir], "$DRIVE$:\\$FILE1$")
    assert at.source == [ "R:\\" ]
    assert at.target == [ "R:\\", "R:\\" ]
    assert at.file == "R:\\abc.def"
    assert at.method == "ZIP"
    assert at.refresh == True

def test_dry_run(empty_test_file):
    zip_file = path.join(conftest.get_tests_dir(), empty_test_file + ".zip")
    at = ArchiveTask("dry-run test sync file", {}, empty_test_file, conftest.get_tests_dir(), zip_file)
    at.run(True)
    assert path.exists(zip_file) == False

def test_real_run(cars_directory_structure):
    paths_map = { 'TEMP': conftest.get_tests_dir(), 'SBR': 'subaru', 'PUG': 'peugeot' }
    src = [
        path.join(cars_directory_structure,'$SBR$'),
        path.join(cars_directory_structure,'$PUG$','106')
    ]
    conftest.process_dir("copy 1", {}, cars_directory_structure)
    conftest.process_dir("copy 2", {}, cars_directory_structure)
    conftest.process_dir("copy 3", {}, cars_directory_structure)
    target = [
        path.join(cars_directory_structure,'copy 1'),
        path.join(cars_directory_structure,'copy 2'),
        path.join(cars_directory_structure,'copy 2'), #test overwriting
        path.join(cars_directory_structure,'copy 3')
    ]
    zip_file = "complex_test.zip"

    at = ArchiveTask("real run", paths_map, src, target, zip_file)
    at.run(False)
    assert path.exists(path.join(target[0],zip_file))
    assert path.exists(path.join(target[1],zip_file))
    assert path.exists(path.join(target[2],zip_file))
    assert not path.exists(path.join(conftest.get_tests_dir(),zip_file))

    conftest.process_dir("assert", {}, cars_directory_structure)
    x_cmd = at.ZIP_UTIL + " x \"" + path.join(path.join(target[0],zip_file)) + "\" -o" + path.join(cars_directory_structure,"assert")
    subprocess.call(x_cmd, shell=True)
    assert path.exists(path.join(cars_directory_structure,"assert","subaru","BRZ.txt"))
    assert path.exists(path.join(cars_directory_structure,"assert","subaru","WRX.txt"))
    assert path.exists(path.join(cars_directory_structure,"assert","subaru","Impreza.txt"))
    assert path.exists(path.join(cars_directory_structure,"assert","106","106-xs.txt"))
    assert path.exists(path.join(cars_directory_structure,"assert","106","106-grd.txt"))
    assert not path.exists(path.join(cars_directory_structure,"assert","106","205-gti.txt"))
    assert not path.exists(path.join(cars_directory_structure,"assert","RCZ.txt"))

def test_no_refresh(cars_directory_structure):
    paths_map = { 'TEMP': conftest.get_tests_dir() }
    src = cars_directory_structure
    conftest.process_dir("copy", {}, cars_directory_structure)
    target = path.join(cars_directory_structure,'copy')
    zip_file = "no_refresh_test.zip"
    zip_file_path = path.join(target,zip_file)
    res = subprocess.call("copy /b NUL " + zip_file_path, shell=True)

    at = ArchiveTask("no refresh test", paths_map, src, target, zip_file, refresh=False)
    at.run(False)
    assert path.exists(zip_file_path)
    assert stat(zip_file_path).st_size == 0