FROM lassoan/slicer-notebook:5.0.2

COPY requirements.txt /app/requirements.txt
RUN /home/sliceruser/Slicer/bin/PythonSlicer -m pip install -r /app/requirements.txt
USER root