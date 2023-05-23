import io
import os
import nrrd
from stl import mesh
import numpy as np
import supervisely as sly
from stl import Mode, mesh
from supervisely.io.fs import get_file_name_with_ext, silent_remove, remove_dir
from supervisely.volume_annotation.volume_annotation import KeyIdMap
from supervisely.geometry.mask_3d import PointLocation3D

import slicer


def segment_object(vol_seg_mask_shape, volume_annotation, volume_object, key_id_map):
    mask = np.zeros(vol_seg_mask_shape).astype(np.bool)
    mask_2d = segment_2d(volume_annotation, volume_object, key_id_map, vol_seg_mask_shape)
    mask = np.where(mask_2d != 0, mask_2d, mask)
    return mask


def segment_2d(volume_annotation, volume_object, key_id_map, vol_seg_mask_shape):
    mask = np.zeros(vol_seg_mask_shape).astype(np.bool)
    volume_object_key = key_id_map.get_object_id(volume_object._key)
    for plane in ["plane_sagittal", "plane_coronal", "plane_axial"]:
        for vol_slice in getattr(volume_annotation, plane):
            vol_slice_id = vol_slice.index
            for figure in vol_slice.figures:
                figure_vobj_key = key_id_map.get_object_id(figure.volume_object._key)
                sly.logger.info(f"Geometry type: {figure.volume_object.obj_class.geometry_type}")
                if figure_vobj_key != volume_object_key:
                    continue
                if figure.volume_object.obj_class.geometry_type not in (sly.Bitmap, sly.Mask3D):
                    figure = convert_to_bitmap(figure)
                try:
                    slice_geometry = figure.geometry
                    slice_bitmap = slice_geometry.data.astype(mask.dtype)
                    sly.logger.info(f"slice_bitmap: {slice_bitmap}")
                    if figure.volume_object.obj_class.geometry_type == sly.Mask3D:
                        bitmap_origin = slice_geometry.space_origin
                    else:
                        bitmap_origin = slice_geometry.origin
                    sly.logger.info(f"bitmap_origin: {bitmap_origin}")

                    slice_bitmap = np.fliplr(slice_bitmap)
                    slice_bitmap = np.rot90(slice_bitmap, 1)

                    mask = draw_figure_on_slice(
                        mask, plane, vol_slice_id, slice_bitmap, bitmap_origin
                    )
                    sly.logger.info(f"mask: {mask}")
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
    masterVolumeNode = slicer.util.loadVolume(volume_path, {"singleFile": True})
    segmentationNode = slicer.util.loadSegmentation(mask_path)

    # Create segment editor to get access to effects
    segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
    sly.logger.info(f"!!!!!!!!!!!!!!! segmentEditorWidget PASSED")
    # To show segment editor widget (useful for debugging): segmentEditorWidget.show()
    segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
    sly.logger.info(f"!!!!!!!!!!!!!!! segmentEditorWidget.setMRMLScene PASSED")
    segmentEditorNode = slicer.vtkMRMLSegmentEditorNode()
    sly.logger.info(f"!!!!!!!!!!!!!!! segmentEditorNode PASSED")
    slicer.mrmlScene.AddNode(segmentEditorNode)
    sly.logger.info(f"!!!!!!!!!!!!!!! slicer.mrmlScene.AddNode PASSED")
    segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
    sly.logger.info(f"!!!!!!!!!!!!!!! setMRMLSegmentEditorNode PASSED")
    segmentEditorWidget.setSegmentationNode(segmentationNode)
    sly.logger.info(f"!!!!!!!!!!!!!!! setSegmentationNode PASSED")
    segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)
    sly.logger.info(f"!!!!!!!!!!!!!!! setMasterVolumeNode PASSED")

    # Run segmentation
    segmentEditorWidget.setActiveEffectByName("Fill between slices")
    sly.logger.info(f"!!!!!!!!!!!!!!! setActiveEffectByName PASSED")
    effect = segmentEditorWidget.activeEffect()
    sly.logger.info(f"!!!!!!!!!!!!!!! effect PASSED")
    # You can change parameters by calling: effect.setParameter("MyParameterName", someValue)
    # Most effect don't have onPreview, you can just call onApply
    sly.logger.info(f"!!!!!!!!!!!!!!! {effect}")
    effect.self().onPreview()
    sly.logger.info(f"!!!!!!!!!!!!!!! effect.self().onPreview() PASSED")
    effect.self().onApply()
    sly.logger.info(f"!!!!!!!!!!!!!!! effect.self().onApply() PASSED")

    segmentationNode.CreateClosedSurfaceRepresentation()
    sly.logger.info(f"!!!!!!!!!!!!!!! CreateClosedSurfaceRepresentation PASSED")
    slicer.vtkSlicerSegmentationsModuleLogic.ExportSegmentsClosedSurfaceRepresentationToFiles(
        output_dir, segmentationNode, None, "STL"
    )
    sly.logger.info(
        f"!!!!!!!!!!!!!!! slicer.vtkSlicerSegmentationsModuleLogic.ExportSegmentsClosedSurfaceRepresentationToFiles PASSED"
    )
    output_mesh_filename = os.listdir(output_dir)[0]
    output_mesh_path = os.path.join(output_dir, output_mesh_filename)
    sly.logger.info(f"!!!!!!!!!!!!!!! output_mesh_path: {output_mesh_path}")

    stl_mesh = mesh.Mesh.from_file(output_mesh_path)
    stl_mesh.save(output_mesh_path, mode=Mode.ASCII)
    stl_mesh = io.open(output_mesh_path, mode="r", encoding="utf-8").read()
    sly.logger.info(f"Interpolation done: {output_mesh_filename}")
    silent_remove(output_mesh_path)
    # sly.logger.info(f"{stl_mesh}")
    return stl_mesh


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
        if sf.geometry.geometry_name() == "mask_3d":
            figure_id = key_id_map.get_figure_id(sf.key())
            figure_path = "{}_mask3d/".format(volume_path[:-5]) + f"{figure_id}.nrrd"
            api.volume.figure.download_stl_meshes([figure_id], [figure_path])
            mask3d_data, mask3d_header = nrrd.read(figure_path)
            sf.geometry.data = mask3d_data
            sf.geometry.space = mask3d_header["space"]
            sf.geometry.space_origin = PointLocation3D(
                col=mask3d_header["space origin"][0],
                row=mask3d_header["space origin"][1],
                tab=mask3d_header["space origin"][2],
            )
            sf.geometry.space_directions = mask3d_header["space directions"]
            path_without_filename = "/".join(figure_path.split("/")[:-1])
            remove_dir(path_without_filename)

    return volume_path, volume_annotation, key_id_map


def draw_annotation(volume_path, volume_annotation, object_id, input_dir, output_dir, key_id_map):
    nrrd_header = nrrd.read_header(volume_path)
    sly.logger.info("Draw mask from annotation")
    for v_object in volume_annotation.objects:
        if key_id_map.get_object_id(v_object._key) != object_id:
            continue
        output_file_name = f"{v_object._key.hex}.nrrd"
        output_save_path = os.path.join(input_dir, output_file_name)

        if v_object.obj_class._geometry_type == sly.Mask3D:
            volume_object_key = key_id_map.get_object_id(v_object._key)
            masks = []
            for sp_figure in volume_annotation.spatial_figures:
                figure_vobj_key = key_id_map.get_object_id(sp_figure.volume_object._key)
                if figure_vobj_key == volume_object_key:
                    masks.append(sp_figure.geometry.data)
            if len(masks) > 1:
                curr_obj_mask = merge_masks(masks)
            else:
                curr_obj_mask = masks[0]
        else:
            curr_obj_mask = segment_object(
                nrrd_header["sizes"], volume_annotation, v_object, key_id_map
            )
        save_nrrd_mask(nrrd_header, curr_obj_mask.astype(np.short), output_save_path)
        sly.logger.info(f"{output_file_name} has been successfully saved.")
        return fill_between_slices(
            volume_path=volume_path, mask_path=output_save_path, output_dir=output_dir
        )


def merge_masks(masks):
    mask = masks.pop(0)
    while masks:
        mask_add = masks.pop(0)
        mask = np.where(mask != 0, mask, mask_add)
    return mask
