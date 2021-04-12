from typing import Optional
import dill
import dash


def dashapp_serializer(app: dash.Dash) -> dict:
    """Serialize a Dash application.

    Note: not all functionalities are copied.

    :param app: a dash application
    :type app: dash.Dash
    :return: a byte representation of the app
    :rtype: dict
    """
    buffer = {
        'config': {k: app.config.get(k) for k in app.config.keys()},
        'attrs': {
            'index': app.index_string,
            'layout': app.layout,
            'css': app.css,
            'scripts': app.scripts,
        }
    }

    return dill.dumps(buffer)

def dashapp_deserializer(serialized: bytes, **kwargs) -> dash.Dash:
    """Transform a dash application back after `dash_serializer`.

    :param serialized: output obtained from `dash_serializer`
    :type serialized_app: bytes
    :return: dash application
    :rtype: dash.Dash
    """
    buffer = dill.loads(serialized)

    # override with custom settings
    buffer['config'].update(kwargs)

    # fixing url_base_pathname and requests_pathname_prefix ambiguity
    # https://github.com/plotly/dash/issues/364
    if 'url_base_pathname' in buffer['config']:
        del buffer['config']['requests_pathname_prefix']
        del buffer['config']['routes_pathname_prefix']

    # re-create dashappp
    app = dash.Dash(**buffer['config'])

    # apply attributes
    for key, value in buffer['attrs'].items():
        setattr(app, key, value)

    return app

