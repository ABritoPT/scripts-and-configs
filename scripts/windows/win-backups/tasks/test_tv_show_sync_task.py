import pytest
from os import path
from .tv_show_sync_task import TVShowSyncTask
from . import conftest

@pytest.fixture
def paths_map():
    return {
        'TVSHOWS': path.join(conftest.get_tests_dir(), "TV Shows"),
        'TVSHOWS_BCK_1': path.join(conftest.get_tests_dir(), "TV Shows - bck1"),
        'TVSHOWS_BCK_2': path.join(conftest.get_tests_dir(), "TV Shows - bck2")
    }

def test_dry_run(paths_map, tv_shows_directory_structure):
    st = TVShowSyncTask("test_dry_run", paths_map, show_name="Seinfeld")
    st.run(True)
    dst = path.join(paths_map['TVSHOWS_BCK_1'], st.show_name)
    assert path.exists(dst) == False

def test_real_run(paths_map, tv_shows_directory_structure):
    st = TVShowSyncTask("test_real_run", paths_map, show_name="Seinfeld")
    st.run(False)
    show_cpy = path.join(paths_map['TVSHOWS_BCK_1'], st.show_name)
    assert path.exists(show_cpy)
    assert path.exists(path.join(show_cpy,"Season 1","S01E01.mp4"))
    assert path.exists(path.join(show_cpy,"Season 3","S03E02.mp4"))
    assert path.exists(path.join(show_cpy,"seinfeld.nfo"))
    conftest.recurse_delete_dir(paths_map['TVSHOWS_BCK_1'])

def test_paths_setup(paths_map):
    with pytest.raises(ValueError, match="Copies setting not supported: invalid_copy"):
        TVShowSyncTask("test_paths_setup", paths_map, copies='invalid_copy')

    st_dup = TVShowSyncTask("test_paths_setup", paths_map, 'Duplicate', "test_show")
    assert st_dup.name == "TVShow test_paths_setup"
    assert st_dup.source == [ path.join(paths_map['TVSHOWS'], "test_show") ]
    assert st_dup.destination == [ path.join(paths_map['TVSHOWS_BCK_1'], "test_show") ]
    assert st_dup.include_count == 0
    assert not st_dup.include_list
    assert not st_dup.exclude_list
    
    st_tri = TVShowSyncTask("test_paths_setup", paths_map, 'Triplicate', "test_show")
    assert st_tri.name == "TVShow test_paths_setup"
    assert st_tri.source == [ path.join(paths_map['TVSHOWS'], "test_show") ]
    assert st_tri.destination == [
        path.join(paths_map['TVSHOWS_BCK_1'], "test_show"),
        path.join(paths_map['TVSHOWS_BCK_2'], "test_show")
    ]
    assert st_tri.include_count == 0
    assert not st_tri.include_list
    assert not st_tri.exclude_list
    
    st_default = TVShowSyncTask("test_paths_setup", paths_map, show_name="test_show")
    assert st_default.name == "TVShow test_paths_setup"
    assert st_default.source == [ path.join(paths_map['TVSHOWS'], "test_show") ]
    assert st_default.destination == [ path.join(paths_map['TVSHOWS_BCK_1'], "test_show") ]
    assert st_default.include_count == 0
    assert not st_default.include_list
    assert not st_default.exclude_list
    
    st_no_show_name = TVShowSyncTask("test_paths_setup", paths_map)
    assert st_no_show_name.name == "TVShow test_paths_setup"
    assert st_no_show_name.source == [ path.join(paths_map['TVSHOWS'], "test_paths_setup") ]
    assert st_no_show_name.destination == [ path.join(paths_map['TVSHOWS_BCK_1'], "test_paths_setup") ]
    assert st_no_show_name.include_count == 0
    assert not st_no_show_name.include_list
    assert not st_no_show_name.exclude_list
    