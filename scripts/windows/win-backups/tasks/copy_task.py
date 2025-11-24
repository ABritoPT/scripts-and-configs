import logging
import shutil
from os import path

class Copy:
    def __init__(self, name, source, destination, include=[], include_count=0, exclude=[]):
        to_list = lambda v : v if isinstance(v, list) else [v]

        self.logger = logging.getLogger()
        self.name = name
        self.source = to_list(source)
        self.destination = to_list(destination)
        self.include_list = to_list(include)
        self.include_count = include_count
        self.exclude_list = to_list(exclude)

    def run(self, dryRun=True):
        self.logger.info("Running copy task " + self.name)

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