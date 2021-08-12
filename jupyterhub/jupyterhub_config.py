# Configuration file for Jupyter Hub

c = get_config()

import os

## Authentication
# c.Authenticator.admin_users = {'admin'}
# c.JupyterHub.admin_access = True

## Authenticator
c.JupyterHub.authenticator_class = "dummy"
# Use PAMAuthenticator, the default, built-in authenticator

## Docker spawner
c.JupyterHub.spawner_class = "docker"

c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'

# c.DockerSpawner.image = 'jupyter/base-notebook'
c.DockerSpawner.image = 'medialab-notebook'
c.DockerSpawner.network_name = 'media-laboratory_net'

# delete containers when the stop
c.DockerSpawner.remove = True

# user data persistence
# see https://jupyterhub-dockerspawner.readthedocs.io/en/latest/data-persistence.html
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {
    'jupyterhub-user-{username}': notebook_dir,
    'media-laboratory_medialab-assets': '/home/jovyan/medialab-assets'
}
