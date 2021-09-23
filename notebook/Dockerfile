# Set JupyterHub version
# Must match the one in the custom jupyterhub image
ARG JUPYTERHUB_VERSION=1.4.2

FROM jupyter/base-notebook:hub-$JUPYTERHUB_VERSION

USER root

# Install extra packages
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get -y install git cron

# Override default entrypoint to run cron
COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh
ENTRYPOINT ["tini", "-g", "--", "/entrypoint.sh"]

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

# Install MediaLab JupyterLab extension
COPY jupyterlab_medialab-0.1.0-py3-none-any.whl /tmp/jupyterlab_medialab-0.1.0-py3-none-any.whl
# RUN python3 -m pip install jupyterlab
RUN python3 -m pip install /tmp/jupyterlab_medialab-0.1.0-py3-none-any.whl
RUN jupyter labextension enable jupyterlab_medialab && \
    jupyter server extension enable jupyterlab_medialab \
    jupyter lab build

ENV JUPYTER_ENABLE_LAB yes

# Setup extension variables
RUN mkdir /home/jovyan/logs
ENV JUPYTERLAB_SCHEDULER_LOG_PATH /home/jovyan/logs
ENV USER jovyan

USER root

CMD ["/usr/local/bin/start-notebook.sh"]
