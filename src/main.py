import functools

import supervisely as sly
from supervisely.sly_logger import add_default_logging_into_file, logger

import functions as f
import globals as g


def send_error_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        value = None
        try:
            value = func(*args, **kwargs)
        except Exception as e:
            sly.logger.error(f"Error while processing data: {e}")
            request_id = kwargs["context"]["request_id"]
            try:
                g.app.send_response(request_id, data={"error": repr(e)})
            except Exception as ex:
                sly.logger.exception(f"Cannot send error response: {ex}")
        return value

    return wrapper


@g.app.callback("interpolate")
@sly.timeit
@send_error_data
def volume_interpolation(api: sly.Api, task_id, context, state, app_logger):
    volume_path, volume_annotation, key_id_map = f.download_volume(
        api=api,
        project_id=context["projectId"],
        volume_id=state["volumeId"],
        input_dir=g.INPUT_DIR,
    )
    nrrd_bytestring = f.draw_annotation(
        volume_path=volume_path,
        volume_annotation=volume_annotation,
        object_id=state["objectId"],
        input_dir=g.INPUT_DIR,
        output_dir=g.OUTPUT_DIR,
        key_id_map=key_id_map,
    )

    logger.info("Start response")
    g.app.send_response(
        request_id=context["request_id"],
        data={"interpolatedBytestring": nrrd_bytestring, "success": True, "error": None},
    )
    logger.info("Finish response")


def main():
    sly.logger.info(
        "Script arguments",
        extra={"context.teamId": g.TEAM_ID, "context.workspaceId": g.WORKSPACE_ID},
    )

    add_default_logging_into_file(logger, log_dir=g.app_root_directory)
    logger.info("🟩 App has been successfully deployed")
    g.app.run()


if __name__ == "__main__":
    sly.main_wrapper("main", main)
