from typing import Optional, Any
import dill
import dash
from .utils import _is_function


# highly inspired by dashserve's serializer
# https://github.com/omegaml/dashserve/blob/master/dashserve/serializer.py
def dashapp_serializer(app: dash.Dash) -> dict:
    """Serialize a Dash application.

    :param app: a dash application
    :type app: dash.Dash
    :return: a byte representation of the app
    :rtype: dict
    """
    cbregistry = dict()
    for cid, cvalue in app.callback_map.items():
        cbregistry[cid] = {
            'inputs': cvalue['inputs'],
            'state': cvalue['state']
        }
        if 'callback' in cvalue:
            cbregistry[cid]['callback'] = dill.dumps(cvalue['callback'])

    buffer = {
        'config': {k: app.config.get(k) for k in app.config.keys()},
        'attrs': {
            'index_string': app.index_string,
            'layout': app.layout,
            '_callback_list': app._callback_list,
            '_inline_scripts': app._inline_scripts
        },
        'cbregistry': cbregistry
    }

    return dill.dumps(buffer)

def dashapp_deserializer(serialized: bytes, **kwargs) -> dash.Dash:
    """Transform a dash application back after being serialized with `dash_serializer`.

    :param serialized: output obtained from `dash_serializer`
    :type serialized_app: bytes
    :return: dash application
    :rtype: dash.Dash
    """
    buffer = dill.loads(serialized)

    # override with custom settings
    # custom settings can also contain functions, with the aim
    # to modify the a config based on app current config value.
    for key, value in kwargs.items():
        if _is_function(value) and (key in buffer['config']):
            buffer['config'][key] = value(buffer['config'].get(key))
        else:
            buffer['config'][key] = value

    # override with custom settings
    # buffer['config'].update(kwargs)

    # fixing url_base_pathname and requests_pathname_prefix ambiguity
    # https://github.com/plotly/dash/issues/364
    if ('url_base_pathname' in buffer['config']) and (buffer['config']['url_base_pathname']):
        del buffer['config']['requests_pathname_prefix']
        del buffer['config']['routes_pathname_prefix']

    # re-create dashappp
    app = dash.Dash(**buffer['config'])

    # apply attributes
    for key, value in buffer['attrs'].items():
        setattr(app, key, value)

    # register callbacks
    cbregistry = buffer.get('cbregistry', {})
    for cid, cvalue in cbregistry.items():
        app.callback_map[cid] = {
            'inputs': cvalue['inputs'],
            'state': cvalue['state']
        }
        if 'callback' in cvalue:
            app.callback_map[cid]['callback'] = dill.loads(cvalue['callback'])

    return app

def get_attr_from_serialized_dashapp(serialized: bytes, attr: str) -> Any:
    """Get one attribute from a serialized dash app without build it entirely.

    Valid attributes are: index_string, layout, css, scripts.

    :param serialized: output obtained from `dash_serializer`
    :type serialized: bytes
    :param attr: attribute's name
    :type attr: str
    :return: attribute's value
    :rtype: Any
    """
    buffer = dill.loads(serialized)

    return buffer['attrs'].get(attr)
