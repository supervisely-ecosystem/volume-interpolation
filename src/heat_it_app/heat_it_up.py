import os
import numpy as np
import supervisely as sly
import functions as f
import globals as g
import json
import nrrd
import uuid
from pathlib import Path
from supervisely.io.fs import silent_remove

work_directory = str(Path(__file__).absolute().parents[0]) + "/"

json_file_paths = [
    "annotation.json",
    "meta.json",
    "key_id_map.json",
]
request_id = str(uuid.uuid4())


def read_json_file(file_path):
    with open(work_directory + file_path, "r") as file:
        data = json.load(file)
    return data


def prepare_data():
    jsons = {}
    for file in json_file_paths:
        key = file.split(".")[0]
        jsons[key] = read_json_file(file)
    return jsons


@f.measure_time
def heat_it_up():
    sly.logger.info("🔥 Start heating up the app")
    jsons = prepare_data()
    key_id_map = sly.KeyIdMap.load_json(work_directory + json_file_paths[2])
    meta = sly.ProjectMeta.from_json(jsons.get("meta"))
    volume_annotation = sly.VolumeAnnotation.from_json(jsons.get("annotation"), meta)

    nrrd_header = nrrd.read_header(work_directory + "volume.nrrd")
    v_object = volume_annotation.objects.items()[0]
    output_file_name = f"{v_object._key.hex}.nrrd"
    output_save_path = os.path.join(g.INPUT_DIR, output_file_name)
    curr_obj_mask = f.segment_object(nrrd_header["sizes"], volume_annotation, v_object, key_id_map)
    f.save_nrrd_mask(nrrd_header, curr_obj_mask.astype(np.short), output_save_path)
    nrrd_bytes = f.make_interpolation(mask_path=output_save_path, output_dir=g.OUTPUT_DIR)
    silent_remove(output_save_path)
    g.heated = True
    sly.logger.info("💡 App is ready to deploy")
