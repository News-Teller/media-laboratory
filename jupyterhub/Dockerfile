# Set JupyterHub version
# Must match the one in the custom notebook image
ARG JUPYTERHUB_VERSION=1.4.2

FROM jupyterhub/jupyterhub:$JUPYTERHUB_VERSION

# Install packages from requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache -r /tmp/requirements.txt

# Copy JupyterHub configuration
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
