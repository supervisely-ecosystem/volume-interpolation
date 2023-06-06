import os

import supervisely as sly
from supervisely.app.v1.app_service import AppService
from supervisely.io.fs import mkdir
from dotenv import load_dotenv


if sly.is_development():
    load_dotenv("debug.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

app = AppService()
api = sly.Api.from_env()

TASK_ID = int(os.environ["TASK_ID"])
TEAM_ID = int(os.environ["context.teamId"])
WORKSPACE_ID = int(os.environ["context.workspaceId"])

INPUT_DIR = "input"
OUTPUT_DIR = "output"

mkdir(INPUT_DIR, True)
mkdir(OUTPUT_DIR, True)
