import os
import time
import nrrd
import numpy as np
import supervisely as sly
from supervisely.io.fs import get_file_name_with_ext, silent_remove
from supervisely.volume_annotation.volume_annotation import KeyIdMap
from supervisely.geometry.mask_3d import Mask3D
from supervisely.project.volume_project import load_figure_data

import slicer


def segment_object(vol_seg_mask_shape, volume_annotation, volume_object, key_id_map):
    mask = np.zeros(vol_seg_mask_shape).astype(np.bool)
    mask = segment_2d(mask, volume_annotation, volume_object, key_id_map)
    mask = segment_3d(mask, volume_annotation, volume_object, key_id_map)

    return mask


def segment_2d(mask, volume_annotation, volume_object, key_id_map):
    volume_object_key = key_id_map.get_object_id(volume_object._key)
    for plane in ["plane_sagittal", "plane_coronal", "plane_axial"]:
        for vol_slice in getattr(volume_annotation, plane):
            vol_slice_id = vol_slice.index
            for figure in vol_slice.figures:
                figure_vobj_key = key_id_map.get_object_id(figure.volume_object._key)
                if figure_vobj_key != volume_object_key:
                    continue
                if not isinstance(figure.geometry, sly.Bitmap):
                    figure = convert_to_bitmap(figure)
                try:
                    slice_geometry = figure.geometry
                    slice_bitmap = slice_geometry.data.astype(mask.dtype)
                    bitmap_origin = slice_geometry.origin

                    slice_bitmap = np.fliplr(slice_bitmap)
                    slice_bitmap = np.rot90(slice_bitmap, 1)

                    mask = draw_figure_on_slice(
                        mask, plane, vol_slice_id, slice_bitmap, bitmap_origin
                    )
                except Exception as e:
                    sly.logger.warn(
                        f"Skipped {plane} slice: {vol_slice_id} due to error: '{e}'",
                        extra={
                            "object_id": volume_object_key,
                            "figure_id": figure_vobj_key,
                        },
                    )
                    continue
    return mask


def draw_figure_on_slice(mask, plane, vol_slice_id, slice_bitmap, bitmap_origin):
    if plane == "plane_sagittal":
        cur_bitmap = mask[
            vol_slice_id,
            bitmap_origin.col : bitmap_origin.col + slice_bitmap.shape[0],
            bitmap_origin.row : bitmap_origin.row + slice_bitmap.shape[1],
        ]
        cur_bitmap = np.where(slice_bitmap != 0, slice_bitmap, cur_bitmap)
        mask[
            vol_slice_id,
            bitmap_origin.col : bitmap_origin.col + slice_bitmap.shape[0],
            bitmap_origin.row : bitmap_origin.row + slice_bitmap.shape[1],
        ] = cur_bitmap

    elif plane == "plane_coronal":
        cur_bitmap = mask[
            bitmap_origin.col : bitmap_origin.col + slice_bitmap.shape[0],
            vol_slice_id,
            bitmap_origin.row : bitmap_origin.row + slice_bitmap.shape[1],
        ]
        cur_bitmap = np.where(slice_bitmap != 0, slice_bitmap, cur_bitmap)
        mask[
            bitmap_origin.col : bitmap_origin.col + slice_bitmap.shape[0],
            vol_slice_id,
            bitmap_origin.row : bitmap_origin.row + slice_bitmap.shape[1],
        ] = cur_bitmap

    elif plane == "plane_axial":
        cur_bitmap = mask[
            bitmap_origin.col : bitmap_origin.col + slice_bitmap.shape[0],
            bitmap_origin.row : bitmap_origin.row + slice_bitmap.shape[1],
            vol_slice_id,
        ]
        cur_bitmap = np.where(slice_bitmap != 0, slice_bitmap, cur_bitmap)
        mask[
            bitmap_origin.col : bitmap_origin.col + slice_bitmap.shape[0],
            bitmap_origin.row : bitmap_origin.row + slice_bitmap.shape[1],
            vol_slice_id,
        ] = cur_bitmap

    return mask


def convert_to_bitmap(figure):
    obj_class = figure.volume_object.obj_class
    new_obj_class = obj_class.clone(geometry_type=sly.Bitmap)
    volume_object = figure.volume_object
    new_volume_object = volume_object.clone(obj_class=new_obj_class)
    new_geometry = figure.geometry.convert(sly.Bitmap)[0]
    return figure.clone(volume_object=new_volume_object, geometry=new_geometry)


def segment_3d(mask, volume_annotation, volume_object, key_id_map):
    volume_object_key = key_id_map.get_object_id(volume_object._key)
    for sp_figure in volume_annotation.spatial_figures:
        if not isinstance(sp_figure.geometry, sly.Mask3D):
            continue

        figure_vobj_key = key_id_map.get_object_id(sp_figure.volume_object._key)
        if figure_vobj_key == volume_object_key:
            mask = np.where(sp_figure.geometry.data != 0, sp_figure.geometry.data, mask)

    return mask


def save_nrrd_mask(nrrd_header, curr_obj_mask, output_save_path):
    nrrd.write(
        output_save_path,
        curr_obj_mask,
        header={
            "encoding": "gzip",
            "space": nrrd_header["space"],
            "space directions": nrrd_header["space directions"],
            "space origin": nrrd_header["space origin"],
        },
        compression_level=1,
    )


def fill_between_slices(volume_path, mask_path, output_dir):
    sly.logger.info(f"Start interpolation for {mask_path}")
    start_time = time.time()
    masterVolumeNode = slicer.util.loadVolume(volume_path, {"singleFile": True})
    end_time = time.time()
    sly.logger.debug(f"Time for masterVolumeNode: {end_time - start_time}")

    start_time = time.time()
    segmentationNode = slicer.util.loadSegmentation(mask_path)
    end_time = time.time()
    sly.logger.debug(f"Time for segmentationNode: {end_time - start_time}")

    start_time = time.time()
    # Create segment editor to get access to effects
    segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
    end_time = time.time()
    sly.logger.debug(f"Time for segmentEditorWidget: {end_time - start_time}")

    start_time = time.time()
    # To show segment editor widget (useful for debugging): segmentEditorWidget.show()
    segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
    end_time = time.time()
    sly.logger.debug(f"Time for setMRMLScene: {end_time - start_time}")

    start_time = time.time()
    segmentEditorNode = slicer.vtkMRMLSegmentEditorNode()
    end_time = time.time()
    sly.logger.debug(f"Time for vtkMRMLSegmentEditorNode: {end_time - start_time}")

    start_time = time.time()
    slicer.mrmlScene.AddNode(segmentEditorNode)
    end_time = time.time()
    sly.logger.debug(f"Time for AddNode(segmentEditorNode): {end_time - start_time}")

    start_time = time.time()
    segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
    end_time = time.time()
    sly.logger.debug(
        f"Time for setMRMLSegmentEditorNode(segmentEditorNode): {end_time - start_time}"
    )

    start_time = time.time()
    segmentEditorWidget.setSegmentationNode(segmentationNode)
    end_time = time.time()
    sly.logger.debug(f"Time for setSegmentationNode(segmentationNode): {end_time - start_time}")

    start_time = time.time()
    segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)
    end_time = time.time()
    sly.logger.debug(f"Time for setMasterVolumeNode(masterVolumeNode): {end_time - start_time}")

    start_time = time.time()
    # Run segmentation
    segmentEditorWidget.setActiveEffectByName("Fill between slices")
    end_time = time.time()
    sly.logger.debug(
        f"Time for setActiveEffectByName(Fill between slices): {end_time - start_time}"
    )

    start_time = time.time()
    effect = segmentEditorWidget.activeEffect()
    end_time = time.time()
    sly.logger.debug(f"Time for segmentEditorWidget.activeEffect(): {end_time - start_time}")

    start_time = time.time()
    # You can change parameters by calling: effect.setParameter("MyParameterName", someValue)
    # Most effect don't have onPreview, you can just call onApply
    effect.self().onPreview()
    end_time = time.time()
    sly.logger.debug(f"Time for onPreview(): {end_time - start_time}")

    start_time = time.time()
    effect.self().onApply()
    end_time = time.time()
    sly.logger.debug(f"Time for onApply(): {end_time - start_time}")

    start_time = time.time()
    segmentationNode.CreateBinaryLabelmapRepresentation()
    end_time = time.time()
    sly.logger.debug(f"Time for CreateBinaryLabelmapRepresentation(): {end_time - start_time}")

    start_time = time.time()
    # segmentationNode.CreateClosedSurfaceRepresentation()
    slicer.vtkSlicerSegmentationsModuleLogic.ExportSegmentsBinaryLabelmapRepresentationToFiles(
        output_dir, segmentationNode, None, "nrrd", True
    )
    end_time = time.time()
    sly.logger.debug(f"Time for EXPORT: {end_time - start_time}")

    output_nrrd_filename = os.listdir(output_dir)[0]
    output_nrrd_path = os.path.join(output_dir, output_nrrd_filename)
    with open(output_nrrd_path, "rb") as file:
        nrrd_bytes = file.read()
    sly.logger.info(f"Interpolation done: {output_nrrd_filename}")
    silent_remove(output_nrrd_path)
    return nrrd_bytes


def download_volume(api, project_id, volume_id, input_dir):
    project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
    key_id_map = KeyIdMap()
    volume_info = api.volume.get_info_by_id(id=volume_id)
    volume_path = os.path.join(input_dir, volume_info.name)
    if not os.path.exists(volume_path):
        sly.logger.info(f"Downloading volume {get_file_name_with_ext(volume_path)}")
        api.volume.download_path(id=volume_id, path=volume_path, progress_cb=None)
    volume_annotation_json = api.volume.annotation.download(volume_id=volume_id)
    volume_annotation = sly.VolumeAnnotation.from_json(
        data=volume_annotation_json, project_meta=project_meta, key_id_map=key_id_map
    )

    for sf in volume_annotation.spatial_figures:
        if sf.geometry.name() == Mask3D.name():
            load_figure_data(api, volume_path, sf, key_id_map)

    return volume_path, volume_annotation, key_id_map


def draw_annotation(volume_path, volume_annotation, object_id, input_dir, output_dir, key_id_map):
    nrrd_header = nrrd.read_header(volume_path)
    sly.logger.info("Draw mask from annotation")
    for v_object in volume_annotation.objects:
        if key_id_map.get_object_id(v_object._key) != object_id:
            continue
        output_file_name = f"{v_object._key.hex}.nrrd"
        output_save_path = os.path.join(input_dir, output_file_name)

        curr_obj_mask = segment_object(
            nrrd_header["sizes"], volume_annotation, v_object, key_id_map
        )

        save_nrrd_mask(nrrd_header, curr_obj_mask.astype(np.short), output_save_path)
        sly.logger.info(f"{output_file_name} has been successfully saved.")
        return fill_between_slices(
            volume_path=volume_path, mask_path=output_save_path, output_dir=output_dir
        )
