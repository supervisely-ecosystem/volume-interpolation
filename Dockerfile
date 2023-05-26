FROM lassoan/slicer-notebook:5.0.2 as builder

RUN /home/sliceruser/Slicer/bin/PythonSlicer -m pip install \    
    argon2_cffi==21.3.0 \
    asttokens==2.2.1 \    
    black==23.3.0 \    
    click==8.1.3 \
    debugpy==1.6.7 \
    executing==1.2.0 \
    ipython==8.13.2 \
    jedi==0.18.2 \
    matplotlib_inline==0.1.6 \
    pathspec==0.11.1 \
    platformdirs==3.5.1 \
    prompt_toolkit==3.0.38 \
    Pygments==2.15.1 \
    setuptools==67.8.0 \
    stack_data==0.6.2 \
    traitlets==5.9.0 \
    wcwidth==0.2.6 \
    xeus_python_shell==0.5.0

FROM lassoan/slicer-notebook:5.0.2

RUN rm -rf /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/{ \
    argon2, \ 
    asttokens, \     
    black, \
    blackd, \     
    click, \ 
    debugpy, \ 
    executing, \ 
    IPython, \ 
    jedi, \ 
    matplotlib_inline, \ 
    pathspec, \ 
    platformdirs, \ 
    prompt_toolkit, \ 
    pygments, \ 
    setuptools, \ 
    stack_data, \ 
    traitlets, \ 
    wcwidth, \ 
    xeus_python_shell \
    }

RUN rm -rf /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/{ \
    argon2_cffi-20.1.0.dist-info, \
    asttokens-2.0.5.dist-info, \
    black-22.1.0.dist-info, \
    click-8.0.3.dist-info, \
    debugpy-1.5.1.dist-info, \
    executing-0.8.2.dist-info, \
    ipython-8.0.1.dist-info, \
    jedi-0.18.0.dist-info, \
    matplotlib_inline-0.1.3.dist-info, \
    pathspec-0.9.0.dist-info, \
    platformdirs-2.5.0.dist-info, \
    prompt_toolkit-3.0.28.dist-info, \
    Pygments-2.11.2.dist-info, \
    setuptools-60.9.0.dist-info, \
    stack_data-0.2.0.dist-info, \
    traitlets-5.1.1.dist-info, \
    wcwidth-0.2.5.dist-info, \
    xeus_python_shell-0.2.0.dist-info \
    }

COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/argon2 /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/argon2
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/asttokens /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/asttokens
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/black /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/black
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/blackd /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/blackd
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/click /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/click
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/debugpy /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/debugpy
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/executing /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/executing
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/IPython /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/IPython
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/jedi /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/jedi
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/matplotlib_inline /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/matplotlib_inline
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/pathspec /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/pathspec
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/platformdirs /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/platformdirs
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/prompt_toolkit /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/prompt_toolkit
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/pygments /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/pygments
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/setuptools /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/setuptools
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/stack_data /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/stack_data
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/traitlets /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/traitlets
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/wcwidth /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/wcwidth
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/xeus_python_shell /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/xeus_python_shell

COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/argon2_cffi-21.3.0.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/argon2_cffi-21.3.0.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/asttokens-2.2.1.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/asttokens-2.2.1.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/black-23.3.0.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/black-23.3.0.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/click-8.1.3.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/click-8.1.3.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/debugpy-1.6.7.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/debugpy-1.6.7.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/executing-1.2.0.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/executing-1.2.0.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/ipython-8.13.2.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/ipython-8.13.2.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/jedi-0.18.2.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/jedi-0.18.2.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/matplotlib_inline-0.1.6.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/matplotlib_inline-0.1.6.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/pathspec-0.11.1.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/pathspec-0.11.1.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/platformdirs-3.5.1.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/platformdirs-3.5.1.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/prompt_toolkit-3.0.38.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/prompt_toolkit-3.0.38.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/Pygments-2.15.1.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/Pygments-2.15.1.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/setuptools-67.8.0.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/setuptools-67.8.0.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/stack_data-0.6.2.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/stack_data-0.6.2.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/traitlets-5.9.0.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/traitlets-5.9.0.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/wcwidth-0.2.6.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/wcwidth-0.2.6.dist-info
COPY --from=builder /home/sliceruser/Slicer/lib/Python/lib/python3.9/site-packages/xeus_python_shell-0.5.0.dist-info /home/sliceruser/Slicer/NA-MIC/Extensions-30607/SlicerJupyter/lib/python3.9/site-packages/xeus_python_shell-0.5.0.dist-info

RUN /home/sliceruser/Slicer/bin/PythonSlicer -m pip install \
    supervisely==6.72.16 \
    numpy-stl==2.17.1 \
    scikit-video==1.1.11

USER root