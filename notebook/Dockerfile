# Set JupyterHub version
# Must match the one in the custom jupyterhub image
ARG JUPYTERHUB_VERSION=1.4.2

FROM jupyter/base-notebook:hub-$JUPYTERHUB_VERSION

# Install git, required for dataviz package
USER root
RUN apt update
RUN apt-get install -y git
USER jovyan

# Install packages from requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache -r /tmp/requirements.txt

# Set MediaLab environment variables
ENV MONGODB_URI=mongodb://mongodb:27017/
ENV ASSETS_FOLDER=/home/jovyan/work/medialab-assets

RUN mkdir $ASSETS_FOLDER

# Copy 'Getting started'
COPY getting_started.ipynb /home/jovyan/work/
COPY getting_started.py /home/jovyan/work/

VOLUME $ASSETS_FOLDER
