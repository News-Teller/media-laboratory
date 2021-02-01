# Media Laboratory project

Data visualisation tool to share your visual analysis on the Web,
allowing a smooth transition from experiments to production.
Build on top of [Dash](https://github.com/plotly/dash) and [Gunicorn](https://github.com/benoitc/gunicorn).

## Overview

The main use case proceed as follow:

0. analyse data, transform it and finalise the best visualisation

1. deploy the visualisation and obtain an ID

2. use the given ID to access the visualisation on the Web

## Usage

1. Clone this repo and copy `notebook` folder inside your Jupyter working directory.

```bash
cd media-laboratory
cp -r notebook YOUR_JUPYTER_FOLDER
```

2. Run the server (development mode)

```bash
cd server
pip install -r requirements.txt
docker run -p "27017:27017" -e MONGO_INITDB_DATABASE=notebook mongo:4.4
python index.py
```

Docker is used to spawn up a MongoDB instance. Feel free to omit that command if you want to use your own database.

To run the server in production mode instead:

```bash
cd server
docker build -t medialab-server .
docker run -p "27017:27017" -e MONGO_INITDB_DATABASE=notebook --net=medialab mongo:4.4
docker run -p 8080:8080 -e MONGODB_URI=mongodb://mongodb:27017/ --net=medialab medialab-server
```

3. Run the example notebook `example_notebook.ipynb`.

## Contributions

Please use [issues](https://github.com/News-Teller/media-laboratory/issues)
to suggest changes and [pull requests](https://github.com/News-Teller/media-laboratory/pulls)
to suggest implementations of changes.

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details on contribution process.
