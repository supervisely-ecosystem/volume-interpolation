import os
from pathlib import Path
import sys

import supervisely as sly
from supervisely.sly_logger import logger
from supervisely.app.v1.app_service import AppService

from supervisely.volume_annotation.volume_annotation import KeyIdMap

app_root_directory = str(Path(__file__).parent.absolute().parents[0])
logger.info(f"App root directory: {app_root_directory}")
sys.path.append(app_root_directory)
sys.path.append(os.path.join(app_root_directory, "src"))
logger.info(f'PYTHONPATH={os.environ.get("PYTHONPATH", "")}')

# order matters
from dotenv import load_dotenv
load_dotenv(os.path.join(app_root_directory, "secret_debug.env"))
load_dotenv(os.path.join(app_root_directory, "debug.env"))



app = AppService()
api = sly.Api.from_env()



TASK_ID = int(os.environ["TASK_ID"])
TEAM_ID = int(os.environ["context.teamId"])
WORKSPACE_ID = int(os.environ["context.workspaceId"])
PROJECT_ID = int(os.environ["context.projectId"])
KEY_ID_MAP = KeyIdMap()

INPUT_DIR = os.path.join(app_root_directory, "input")
OUTPUT_DIR = os.path.join(app_root_directory, "output")

project = api.project.get_info_by_id(PROJECT_ID)
project_meta = sly.ProjectMeta.from_json(api.project.get_meta(PROJECT_ID))
