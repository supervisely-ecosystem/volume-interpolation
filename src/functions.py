import nrrd
import numpy as np
import supervisely as sly
from supervisely.io.fs import get_file_name_with_ext

import slicer


def segment_object(vol_seg_mask_shape, volume_annotation, volume_object, key_id_map):
    mask = np.zeros(vol_seg_mask_shape).astype(np.bool)
    mask_2d = segment_2d(
        volume_annotation, volume_object, key_id_map, vol_seg_mask_shape
    )
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
                if figure_vobj_key != volume_object_key:
                    continue
                if figure.volume_object.obj_class.geometry_type != sly.Bitmap:
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
                     bitmap_origin.col: bitmap_origin.col + slice_bitmap.shape[0],
                     bitmap_origin.row: bitmap_origin.row + slice_bitmap.shape[1],
                     ]
        cur_bitmap = np.where(slice_bitmap != 0, slice_bitmap, cur_bitmap)
        mask[
        vol_slice_id,
        bitmap_origin.col: bitmap_origin.col + slice_bitmap.shape[0],
        bitmap_origin.row: bitmap_origin.row + slice_bitmap.shape[1],
        ] = cur_bitmap

    elif plane == "plane_coronal":
        cur_bitmap = mask[
                     bitmap_origin.col: bitmap_origin.col + slice_bitmap.shape[0],
                     vol_slice_id,
                     bitmap_origin.row: bitmap_origin.row + slice_bitmap.shape[1],
                     ]
        cur_bitmap = np.where(slice_bitmap != 0, slice_bitmap, cur_bitmap)
        mask[
        bitmap_origin.col: bitmap_origin.col + slice_bitmap.shape[0],
        vol_slice_id,
        bitmap_origin.row: bitmap_origin.row + slice_bitmap.shape[1],
        ] = cur_bitmap

    elif plane == "plane_axial":
        cur_bitmap = mask[
                     bitmap_origin.col: bitmap_origin.col + slice_bitmap.shape[0],
                     bitmap_origin.row: bitmap_origin.row + slice_bitmap.shape[1],
                     vol_slice_id,
                     ]
        cur_bitmap = np.where(slice_bitmap != 0, slice_bitmap, cur_bitmap)
        mask[
        bitmap_origin.col: bitmap_origin.col + slice_bitmap.shape[0],
        bitmap_origin.row: bitmap_origin.row + slice_bitmap.shape[1],
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


def fill_between_slices(volume_path, mask_path):
    sly.logger("start interpolation")
    masterVolumeNode = slicer.util.loadVolume(volume_path, {"singleFile": True})
    segmentationNode = slicer.util.loadSegmentation(mask_path)

    # slicer.util.exportNode(loadedVolumeNode, "/app/input/MRHead.nrrd")

    # Create segment editor to get access to effects
    segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
    # To show segment editor widget (useful for debugging): segmentEditorWidget.show()
    segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
    segmentEditorNode = slicer.vtkMRMLSegmentEditorNode()
    slicer.mrmlScene.AddNode(segmentEditorNode)
    segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
    segmentEditorWidget.setSegmentationNode(segmentationNode)
    segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)

    # Run segmentation
    segmentEditorWidget.setActiveEffectByName("Fill between slices")
    effect = segmentEditorWidget.activeEffect()
    # You can change parameters by calling: effect.setParameter("MyParameterName", someValue)
    # Most effect don't have onPreview, you can just call onApply
    effect.self().onPreview()
    effect.self().onApply()

    output_path = f"/app/output/{get_file_name_with_ext(mask_path)}"
    slicer.util.exportNode(segmentationNode, output_path)


# 1) check 1 object 3 figs +++
# 2) check 1 object different axes different slices ---
