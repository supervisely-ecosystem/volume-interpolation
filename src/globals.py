import os
import supervisely as sly
from supervisely.io.fs import mkdir
from dotenv import load_dotenv

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if sly.is_development():
    load_dotenv("debug.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api.from_env()

TASK_ID = int(os.environ["TASK_ID"])
TEAM_ID = int(os.environ["context.teamId"])
WORKSPACE_ID = int(os.environ["context.workspaceId"])

INPUT_DIR = os.path.join(main_dir, "input")
OUTPUT_DIR = os.path.join(main_dir, "output")

mkdir(INPUT_DIR, True)
mkdir(OUTPUT_DIR, True)

heated = False
