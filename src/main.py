import supervisely as sly
from supervisely.sly_logger import logger
import functools
import globals as g
import functions as f


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
    logger.info("Download volume")
    volume_path, volume_annotation = f.download_volume(
        volume_id=state["volumeId"], input_dir=g.INPUT_DIR
    )

    logger.info("Start interpolation")
    stl_mesh = f.draw_annotation(
        volume_path=volume_path,
        volume_annotation=volume_annotation,
        object_id=state["objectId"],
        input_dir=g.INPUT_DIR,
        output_dir=g.OUTPUT_DIR,
        key_id_map=g.KEY_ID_MAP,
    )

    logger.info("Send response")
    g.app.send_response(
        request_id=context["request_id"],
        data={
            "interpolatedStl": stl_mesh,
            "success": True,
            "error": None,
        },
    )


def main():
    sly.logger.info(
        "Script arguments",
        extra={
            "context.teamId": g.TEAM_ID,
            "context.workspaceId": g.WORKSPACE_ID,
        },
    )

    g.app.run()


if __name__ == "__main__":
    sly.main_wrapper("main", main)
