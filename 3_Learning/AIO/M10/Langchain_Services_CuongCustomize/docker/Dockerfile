FROM python:3.11-slim

WORKDIR /backend

# Install system dependencies required for OpenCV and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./docker/requirements.txt .

RUN pip install --upgrade wheel setuptools pip \
    && pip install -r requirements.txt --no-cache-dir

COPY /data_source /backend/data_source

COPY /src /backend/src

WORKDIR /backend
