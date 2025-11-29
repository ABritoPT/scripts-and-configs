import logging
import sys
import yaml

from tasks.script_task import ScriptTask
from tasks.sync_task import SyncTask
from tasks.tv_show_sync_task import TVShowSyncTask
from tasks import task_utils

TEST_JOB='d:/André/coding/sensitive/main-backup-job.yaml'
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
