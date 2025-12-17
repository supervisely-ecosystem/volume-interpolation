FROM python:3.9.23

# Install system dependencies for OpenCV headless operation
RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for headless operation
ENV QT_QPA_PLATFORM=offscreen
ENV DISPLAY=:99

RUN pip install --upgrade pip 

COPY dev_requirements.txt /req/dev_requirements.txt

RUN pip install --no-cache-dir --disable-pip-version-check -r /req/dev_requirements.txt

LABEL python_sdk_version="6.73.486"
