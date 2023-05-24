FROM lassoan/slicer-notebook:5.0.2

RUN /home/sliceruser/Slicer/bin/PythonSlicer -m pip install pygments==2.15.1 supervisely==6.72.16 numpy-stl==2.17.1 scikit-video==1.1.11
USER root