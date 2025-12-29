import logging
import shutil
from os import path
from . import task_utils

class SyncTask:
    def __init__(self, name: str, paths_map: dict[str,str], source: str|list[str],
                 destination: str|list[str], include: list[str] = [], include_count: int = 0,
                 exclude: list[str] = []):
        self.logger = logging.getLogger()
        self.name = name
        self.source = task_utils.prep_path_param(source, paths_map)
        self.destination = task_utils.prep_path_param(destination, paths_map)
        self.include_list = task_utils.prep_path_param(include, paths_map)
        self.exclude_list = task_utils.prep_path_param(exclude, paths_map)
        self.include_count = include_count

    def run(self, dryRun: bool = True):
        self.logger.info("Running sync task " + self.name)

        task_res = 0
        for src in self.source:
            if not path.exists(src):
                raise ValueError("Path does not exist: " + src)
            # if len(self.include_list) != 0:
            # if len(self.exclude_list) != 0:
            for dst in self.destination:
                if dryRun:
                    self.logger.info("Dry run - no action taken")
                else:
                    self.logger.info("Copying " + src + " to " + dst)
                    if path.isdir(src):
                        shutil.copytree(src,dst,dirs_exist_ok=True)
                    else:
                        shutil.copy2(src,dst)
                    self.logger.info("Copy successful")
        
        return task_res