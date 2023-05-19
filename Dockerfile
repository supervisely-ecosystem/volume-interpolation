FROM lassoan/slicer-notebook:5.0.2

RUN /home/sliceruser/Slicer/bin/PythonSlicer -m pip install git+https://github.com/supervisely/supervisely.git@add-bitmap3d-geometry numpy-stl==2.17.1 scikit-video==1.1.11
USER root