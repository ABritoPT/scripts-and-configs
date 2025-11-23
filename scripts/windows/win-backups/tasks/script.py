import logging
import subprocess

class Script:
    def __init__(self, name, target, start_in=None, timing=None):
        self.logger = logging.getLogger()
        self.name = name
        self.target = target
        self.start_in = start_in
        self.timing = timing
    
    def run(self, dryRun=True):
        self.logger.info("Running script task " + self.name)

        command = ""
        if self.start_in:
            command += "cd /d " + self.start_in + " & "
        command += self.target
        self.logger.debug("Command: " + command)

        if dryRun:
            self.logger.info("Dry run - no action taken")
        else:
            self.logger.info("executing " + command)
            res = subprocess.call(command, shell=True)
            self.logger.info("Success" if res == 0 else "Command failed")

# 2 ways to run commands:
# os.system('start cmd /k "cd /d D:\\André\\_dumps & dir')
# subprocess.call("cd /d D:\\André\\_dumps & D:\\André\\_dumps\\_run.bat", shell=True)