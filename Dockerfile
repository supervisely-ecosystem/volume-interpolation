FROM lassoan/slicer-notebook:5.0.2

RUN /home/sliceruser/Slicer/bin/PythonSlicer -m pip install supervisely==6.29.0 supervisely[apps]==6.29.0 numpy-stl==2.17.1 scikit-video==1.11.1
RUN pwd && exit 1