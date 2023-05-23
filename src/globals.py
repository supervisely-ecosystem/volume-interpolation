import os
import sys
from pathlib import Path

import supervisely as sly
from supervisely.app.v1.app_service import AppService
from supervisely.io.fs import mkdir
from supervisely.sly_logger import logger


app_root_directory = str(Path(__file__).parent.absolute().parents[0])
logger.info(f"App root directory: {app_root_directory}")
sys.path.append(app_root_directory)
sys.path.append(os.path.join(app_root_directory, "src"))
logger.info(f'PYTHONPATH={os.environ.get("PYTHONPATH", "")}')

# order matters
# from dotenv import load_dotenv
# load_dotenv(os.path.join(app_root_directory, "secret_debug.env"))
# load_dotenv(os.path.join(app_root_directory, "debug.env"))

app = AppService()
api = sly.Api.from_env()

TASK_ID = int(os.environ["TASK_ID"])
TEAM_ID = int(os.environ["context.teamId"])
WORKSPACE_ID = int(os.environ["context.workspaceId"])

STORAGE_DIR = "/home/sliceruser"
INPUT_DIR = os.path.join(STORAGE_DIR, "input")
OUTPUT_DIR = os.path.join(STORAGE_DIR, "output")

mkdir(INPUT_DIR, True)
mkdir(OUTPUT_DIR, True)
