FROM lassoan/slicer-notebook:5.0.2

RUN /home/sliceruser/Slicer/bin/PythonSlicer -m pip install supervisely==6.31.0 supervisely[apps]==6.31.0 numpy-stl==2.17.1 scikit-video==1.1.11

USER root