import os
from pathlib import Path

import nrrd
import numpy as np
import supervisely as sly
from dotenv import load_dotenv
from supervisely.volume_annotation.volume_annotation import KeyIdMap

import functions as f

app_root_directory = str(Path(__file__).parent.absolute().parents[0])
sly.logger.info(f"App root directory: {app_root_directory}")


load_dotenv(os.path.join(app_root_directory, "debug.env"))
load_dotenv(os.path.join(app_root_directory, "secret_debug.env"))

api = sly.Api.from_env()
project_id = 11999
volume_id = 3051131
object_id = 3859225
key_id_map = KeyIdMap()

project = api.project.get_info_by_id(project_id)
project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))

input_dir = "/app/input"
output_dir = "/app/output"


# input_dir = "../input"
# output_dir = "../output"


def download_volume(volume_id, input_dir):
    volume_info = api.volume.get_info_by_id(id=volume_id)
    volume_path = os.path.join(input_dir, volume_info.name)
    api.volume.download_path(id=volume_id, path=volume_path, progress_cb=None)
    volume_annotation_json = api.volume.annotation.download(volume_id=volume_id)
    volume_annotation = sly.VolumeAnnotation.from_json(
        data=volume_annotation_json, project_meta=project_meta, key_id_map=key_id_map
    )
    return volume_path, volume_annotation


def draw_annotation(volume_path, volume_annotation, input_dir, key_id_map):
    nrrd_header = nrrd.read_header(volume_path)
    for v_object in volume_annotation.objects:
        if key_id_map.get_object_id(v_object._key) != object_id:
            continue
        output_file_name = f"{v_object._key.hex}.nrrd"
        output_save_path = os.path.join(input_dir, output_file_name)

        curr_obj_mask = f.segment_object(
            nrrd_header["sizes"], volume_annotation, v_object, key_id_map
        )
        f.save_nrrd_mask(nrrd_header, curr_obj_mask.astype(np.short), output_save_path)
        f.fill_between_slices(volume_path=volume_path, mask_path=output_save_path)


def main():
    volume_path, volume_annotation = download_volume(
        volume_id=volume_id, input_dir=input_dir
    )
    draw_annotation(
        volume_path=volume_path,
        volume_annotation=volume_annotation,
        input_dir=input_dir,
        key_id_map=key_id_map,
    )


main()
