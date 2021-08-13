# Media Laboratory project

Data visualisation tool to share your visual analysis on the Web.
Build on top of [Dash](https://github.com/plotly/dash) and [Gunicorn](https://github.com/benoitc/gunicorn).

# Overview

The main use case proceed as follow:

-   analyse data, transform it and finalise the best visualisation
    using a Jupyter notebook
-   create a Dash application to represent your visualisation and save it
-   access it and share it using its unique identifier

## Deploy

First, build the custom images:

```bash
docker build -t medialab-notebook notebook
docker-compose build
```

Launch the whole stack using [Docker Compose](https://docs.docker.com/compose/):

```bash
docker-compose up -d
```

-   JupyterHub will be available at `http://localhost:8000`
-   visualizations will be available at `http://localhost:8080/<uid>`

### HTTPS

`docker-compose.secure.yml` uses [Caddy](https://github.com/caddyserver/caddy)
as reverse proxy to serve JupyterHub and the python webserver over HTTPS.
You'll need to replace `.your_domain.com` inside [`caddy/Caddyfile`](caddy/Caddyfile) with your registered domain.  
Then, append this second configuration to the base one:

```bash
docker-compose -f docker-compose.yml -f docker-compose.secure.yml up -d
```

## Usage

Access JupyterHub at `http://localhost:8000` and login with your credentials.
Start creating your visualizations in the form of Dash applications
and save them using the [`DataViz`](dataviz.md) python package (already included in the custom docker notebook image).  
After saving, they'll be available on the webserver at `http://localhost:8080/<uid>`,
with `uid` being the visualization unique identifier.

Check the notebook `getting_started.ipynb` for a first overview and
[`dataviz.md`](dataviz.md) for more information on the python package.

## Contributions

Please use [issues](https://github.com/News-Teller/media-laboratory/issues)
to suggest changes and [pull requests](https://github.com/News-Teller/media-laboratory/pulls)
to suggest implementations of changes.

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details on contribution process.

## License

This software is licensed under the terms of the GNU GPLv3. See the [LICENSE](./LICENSE) file for more details.  
Plotly Dash is Copyright (c) 2021 Plotly, Inc, and is not part of the Media Laboratory project.
