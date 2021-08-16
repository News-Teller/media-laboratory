# DataViz

## Usage

### Init

```python
import dataviz
dz = dataviz.DataViz()
```

`DataViz` takes two parameters: the database connection URI (`uri`) and the user (`user`),
however when the environment is properly configured, there's no need to specify them
as they're loaded from the environment variables.

### Publish a visualization

Sore the visualization in the database and make it accessible at `http(s)://<server:port>/<uid>`.

```python
dz.store(
    uid='example',
    title='example viz',
    dash_app=app,
    tags=['notebook', 'example']
)
```

where `app` is your Dash application.  
For a full example, see the `getting_started` notebook on the GitHub repository.

Notes:

-   `uid` can only contain alphanumeric characters, '-' and '\_' ().  
     You can use whatever `uid` you want or generate one randomly using `generate_uid` from `dataviz.utils`.  
     You can use `dz.check_uid_availability(uid='my-id')` to check if it's available.  
     See [Limitations](#limitations) for reserved uids.
-   `tags` are optional and they're used to filter results when listing visualization (see API section).  
     A tag can only contain alphanumeric characters and '-'.

### Static assets

The default folder for static assets is a folder named `medialab-assets/`, placed under the user’s notebook directory
(default to `/home/jovyan/work`).  
To use them with your Dash application you'll need to:

1. create a folder under `medialab-assets/` with the same `uid` of your visualization
2. add your CSS and JavaScript files in this folder
3. specify the `assets_folder` parameter in your Dash application to link to that folder (see example below).

```python
import os

ASSETS_FOLDER = os.getenv('ASSETS_FOLDER', '')

app = jupyter_dash.JupyterDash(
    name='my-uid',
    ...,
    assets_folder=f'{ASSETS_FOLDER}/my-uid'
)
```

_Note_: See [Limitations](#limitations).

### Locked visualizations

A visualization can be locked to prevent unwanted modifications.

```python
dz.store(
    uid='example',
    title='example viz',
    dash_app=app,
    tags=['notebook', 'example'],
    locked=True
)
```

or

```python
dz.lock(uid='example')
```

When trying to update a locked visualization, a `This viz is locked!` exception will block the execution.

To unlock it, use the `unlock` method:

```python
dz.unlock(uid='example')
```

### Restore the previous version

When you update a visualization (call `store` on an existing one),
the previous version is kept in the database as a safe measure.
If you want to restore it, just call the `restore` method:

```python
dz.restore(uid='example')
```

_Note_: you cannot call this method more than once consecutively.

### Delete a visualization

You can deleta visualization with the `delete` method.

```python
dz.delete(uid='example')
```

By default, you will be asked to confirm the deletion by typing `yes` in the python input.
Any other value will abort the operation.

### Get a list of my visualizations

This will return a list of the visualizations created by the logged user.

```python
dz.get_my_visualisations()
```

## API

A simple REST API is available at `http(s)://<server:port>/api/visualizations`,
which lists all visualizations.  
Results can be filtered by using tags, such as: `http(s)://<server:port>/api/visualizations?tags=sport,example`.

## Tips & tricks

-   Use external resources as opposed to local files whenever possible, to speed up the loading time of the visualization
    and to reduce the load on the webserver.  
     For example, you can use services like [jsDelivr](https://www.jsdelivr.com/) to access files from a (public) GitHub repository
    and add them to your Dash app as `external_stylesheets` or `external_scripts`.

-   Published visualizations will load Dash's Component Libraries as bundles from a CDN (`serve_locally=False`).
    To reduce the risk of using different versions of the libraries while developing, set `serve_locally=False` when
    creating your Dash application.

-   If [callbacks](https://dash.plotly.com/basic-callbacks) slow down your visualization,
    try using [clientside callbacks](https://dash.plotly.com/clientside-callbacks).

## Limitations

-   It's not possible to store/publish custom Dash objects, only `dash.Dash` or `jupyter_dash.JupyterDash` work.
-   Some configuration parameters of the Dash application are overriden when loaded back on the webserver.  
     These settings are: `name`, `serve_locally`, `assets_folder`, `requests_pathname_prefix` and `assets_external_path`.  
     Be aware of this while building your application.
    Special mention for `assets_folder`, which can be overriden using the `MAP_ASSETS_FOLDER` environment variable
    to map the orginal path in the notebook environment into the webserver assets path.
-   There are some reserved strings for `uid`: `api` and `static`. Be sure you don't use them.
-   To speed up the loading time of the visualization and reduce the load on the server,
    visualizations are cached for a specific amount of time (see `RETENTION_PERIOD_MIN`).
    This means that changes may take some time to be operational.
