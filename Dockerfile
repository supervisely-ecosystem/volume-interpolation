FROM lassoan/slicer-notebook:5.0.2

RUN /home/sliceruser/Slicer/bin/PythonSlicer -m pip install supervisely==6.72.16 numpy-stl==2.17.1 scikit-video==1.1.11 pygments==2.13.0
USER root