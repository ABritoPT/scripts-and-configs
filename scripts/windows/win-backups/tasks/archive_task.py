import logging
import subprocess
import shutil
from os import path
from . import task_utils

class ArchiveTask:
    ZIP_UTIL = "\"C:\\Program Files\\7-Zip\\7z.exe\""
    ZIP_PARAMS = " a -tzip -r "

    def __init__(self, name: str, paths_map: dict[str,str],
                 source: str|list[str], target: str|list[str],
                 file: str, method: str = "ZIP",
                 refresh: bool = True):
        self.logger = logging.getLogger()
        self.name = name
        self.source = task_utils.prep_path_param(source, paths_map)
        self.target = task_utils.prep_path_param(target, paths_map)
        self.file = task_utils.resolve_placeholders(file, paths_map)
        self.method = method
        self.refresh = refresh
        self.temp = paths_map.get('TEMP')
        # Not implemented: `exclude: str|list[str] = []`
        # https://web.mit.edu/outland/arch/i386_rhel4/build/p7zip-current/DOCS/MANUAL/switches/exclude.htm
        # self.exclude = task_utils.prep_path_param(exclude, paths_map)
    
    def run(self, dryRun: bool = True):
        self.logger.info("Running archive task " + self.name)

        #NOT_IMPLEMENTED method, exclude list

        if self.refresh == False:
            skip = True
            for tar in self.target:
                if path.exists(path.join(tar, self.file)):
                    self.logger.debug("Archive already exists at " + tar)
                else:
                    skip = False
                    break
            if skip:
                self.logger.debug("Archives exist at all targets. Skipping.")
                return 0
        
        for src in self.source:
            if not path.exists(src):
                raise ValueError("Path does not exist: " + src)
        src_list = ' '.join(['"{}"'.format(v) for v in self.source])

        zip_command = ""
        if self.temp:
            if not path.exists(self.temp):
                raise ValueError("Temp folder does not exist: " + self.temp)
            zip_command += "cd /d " + self.temp + " & "
        zip_command += self.ZIP_UTIL + self.ZIP_PARAMS + self.file + ' ' + src_list
        self.logger.debug("Command: " + zip_command)
        
        if dryRun:
            self.logger.info("Dry run - no action taken")
        else:
            self.logger.info("executing " + zip_command)
            res = subprocess.call(zip_command, shell=True)
            self.logger.info("Success" if res == 0 else "Command failed")
            if res != 0: return res
        
        zip_file = path.join(self.temp if self.temp else "", self.file)
        self.logger.debug("Zip file path: " + zip_file)

        for tar in self.target:
            if not path.exists(tar):
                self.logger.warning("Target folder does not exist: " + tar)
                continue
            self.logger.debug("Copying zip file to " + tar)
            if dryRun:
                self.logger.info("Dry run - no action taken")
            else:
                shutil.copy2(zip_file,tar)
                self.logger.info("Copy successful")
        
        self.logger.debug("Deleting Zip file: " + zip_file)
        if dryRun:
            self.logger.info("Dry run - no action taken")
        else:
            subprocess.call("del " + zip_file, shell=True)
            self.logger.info("Deletion successful")
        return 0
