FROM supervisely/base-py-sdk:6.72.32

RUN pip3 install numpy-stl==2.17.1
RUN pip3 install scikit-video==1.1.11
RUN pip3 install itk-morphologicalcontourinterpolation==1.1.0