import os
import sys
from pathlib import Path
from supervisely.sly_logger import logger
import supervisely_lib as sly


def main():
    app_root_directory = str(Path(__file__).parent.absolute().parents[0])
    logger.info(f"App root directory: {app_root_directory}")
    sys.path.append(app_root_directory)
    sys.path.append(os.path.join(app_root_directory, "src"))
    logger.info(f'PYTHONPATH={os.environ.get("PYTHONPATH", "")}')

    # order matters
    from dotenv import load_dotenv
    load_dotenv(os.path.join(app_root_directory, "secret_debug.env"))
    load_dotenv(os.path.join(app_root_directory, "debug.env"))

    api = sly.Api.from_env()
    task_id = int(os.environ["TASK_ID"])
    volume_id = int(os.environ["modal.state.volumeId"])
    object_id = int(os.environ["modal.state.objectId"])

    # context = {"volumeId": volume_id, "objectId": object_id}
    data = {"volumeId": volume_id, "objectId": object_id}

    response = api.task.send_request(task_id, "interpolate", data=data, context={}, timeout=60)
    print("APP returns data:")
    print(response)


if __name__ == "__main__":
    main()
