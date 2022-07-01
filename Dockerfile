FROM lassoan/slicer-notebook:5.0.2

RUN /home/sliceruser/Slicer/bin/PythonSlicer -m pip install supervisely==6.25.0
