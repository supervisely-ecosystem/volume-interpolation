FROM supervisely/3dslicer:1.0.6

COPY requirements.txt /app/requirements.txt
RUN /home/sliceruser/Slicer/bin/PythonSlicer -m pip install -r /app/requirements.txt
USER root