import pytest
import re
import subprocess
from os import path
from . import conftest
from .sync_task import SyncTask

def test_fake_source():
    dir = "ZZZ:\\fake\\folder"
    st = SyncTask("fake source test", dir, dir)
    with pytest.raises(ValueError, match=re.escape("Path does not exist: " + dir)):
        st.run()

def test_dry_run(empty_test_file):
    dst = empty_test_file + ".cpy"
    st = SyncTask("dry-run test sync file", empty_test_file, dst)
    st.run(True)
    assert path.exists(dst) == False

def test_real_run(empty_test_file):
    dst = empty_test_file + ".cpy"
    st = SyncTask("dry-run test sync file", empty_test_file, dst)
    st.run(False)
    assert path.exists(dst) == True
    subprocess.call("del " + dst, shell=True)

def test_complex_sync(cars_directory_structure):
    src = cars_directory_structure
    dst = src + "-copy"
    st = SyncTask("complex sync test", src, dst)
    
    st.run(False)
    assert path.exists(path.join(dst, "subaru", "BRZ.txt")) == True
    assert path.exists(path.join(dst, "peugeot", "205", "205-xs.txt")) == True
    assert path.exists(path.join(dst, "peugeot", "106", "106-grd.txt")) == True
    assert path.exists(path.join(dst, "peugeot", "RCZ.txt")) == True
    
    conftest.recurse_delete_dir(dst)