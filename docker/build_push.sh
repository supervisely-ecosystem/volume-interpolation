cp ../dev_requirements.txt . && \
docker build --no-cache -f Dockerfile -t supervisely/volume-interpolation:1.0.6 .. && \
rm dev_requirements.txt 
docker push supervisely/volume-interpolation:1.0.6