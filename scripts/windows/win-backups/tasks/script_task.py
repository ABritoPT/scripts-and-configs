import logging
import subprocess
import os
from . import task_utils

class ScriptTask:
    def __init__(self, name: str, paths_map: dict[str,str], target: str, start_in: str|None = None, timing: str|None = None):
        self.logger = logging.getLogger()
        self.name = name
        self.target = task_utils.resolve_placeholders(target, paths_map)
        self.start_in = task_utils.resolve_placeholders(start_in, paths_map) if start_in else None
        self.timing = timing
    
    def run(self, dryRun: bool = True):
        self.logger.info("Running script task " + self.name)

        command = ""
        if self.start_in:
            if not os.path.exists(self.start_in):
                raise ValueError("Start in folder does not exist")
            command += "cd /d " + self.start_in + " & "
        command += self.target
        self.logger.debug("Command: " + command)

        if dryRun:
            self.logger.info("Dry run - no action taken")
            return 0
        else:
            self.logger.info("executing " + command)
            res = subprocess.call(command, shell=True)
            self.logger.info("Success" if res == 0 else "Command failed")
            return res

# 2 ways to run commands:
# os.system('start cmd /k "cd /d D:\\André\\_dumps & dir')
# subprocess.call("cd /d D:\\André\\_dumps & D:\\André\\_dumps\\_run.bat", shell=True)