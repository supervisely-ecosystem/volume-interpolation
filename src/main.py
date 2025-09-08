import supervisely as sly
from supervisely.io.fs import clean_dir
from fastapi.responses import StreamingResponse
from fastapi import Request, HTTPException

import src.functions as f
import src.globals as g

from src.heat_it_app.heat_it_up import heat_it_up

app = sly.Application()
server = app.get_server()


@server.post("/interpolate")
async def volume_interpolation(request: Request):
    req = await request.json()
    try:
        state = req["state"]
        context = req.get("context", {})

        volume_path, volume_annotation, key_id_map = f.download_volume(
            api=g.api,
            project_id=context.get("projectId"),
            volume_id=state.get("volumeId"),
            input_dir=g.INPUT_DIR,
        )

        nrrd_bytes = f.draw_annotation(
            volume_path=volume_path,
            volume_annotation=volume_annotation,
            object_id=state.get("objectId"),
            input_dir=g.INPUT_DIR,
            output_dir=g.OUTPUT_DIR,
            key_id_map=key_id_map,
        )

        # Create chunk generator
        def generator():
            chunk_size = 1048576
            for i in range(0, len(nrrd_bytes), chunk_size):
                yield nrrd_bytes[i : i + chunk_size]

        # Return StreamingResponse for FastAPI
        response = StreamingResponse(
            generator(),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": "attachment; filename=interpolation.nrrd",
                "Content-Type": "application/octet-stream",
                "x-request-id": context.get("request_id", ""),
            },
        )

        clean_dir(g.INPUT_DIR)

        return response

    except Exception as e:
        sly.logger.error(f"Error during volume interpolation: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


heat_it_up()
sly.logger.info(
    "Script arguments",
    extra={"context.teamId": g.TEAM_ID, "context.workspaceId": g.WORKSPACE_ID},
)

sly.logger.info("🟩 App has been successfully deployed")
