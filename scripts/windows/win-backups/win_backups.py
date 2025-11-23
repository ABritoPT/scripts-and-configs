import logging
import sys
import yaml

from tasks.script import Script

TEST_JOB='d:/André/coding/git/scripts-and-configs/scripts/windows/win-backups/jobs/main.yaml'
dryRun = True

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(stream=sys.stdout)
# logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
# stream_handler.setFormatter(logFormatter)
logger.addHandler(stream_handler)
logger.debug("logger set")

with open(TEST_JOB, 'r') as file:
    job = yaml.safe_load(file)
# print(job)

sc = Script("test","dir")
# sc = Script("test","D:\André\_dumps\_run.bat","D:\André\_dumps")
sc.run(dryRun)