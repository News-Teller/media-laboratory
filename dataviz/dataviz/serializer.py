from typing import Optional, Any
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
    # pickle callback functions from callback_map
    cbregistry = dict()
    for cid, cvalue in app.callback_map.items():
        cbregistry[cid] = {
            'inputs': cvalue['inputs'],
            'state': cvalue['state'],
            'callback': dill.dumps(cvalue['callback'])
        }

    buffer = {
        'config': {k: app.config.get(k) for k in app.config.keys()},
        'attrs': {
            'index_string': app.index_string,
            'layout': app.layout,
            'css': app.css,
            'scripts': app.scripts,
            '_callback_list': app._callback_list
        },
        'rebuild': {
            'cbregistry': cbregistry
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
    if ('url_base_pathname' in buffer['config']) and (buffer['config']['url_base_pathname']):
        del buffer['config']['requests_pathname_prefix']
        del buffer['config']['routes_pathname_prefix']

    # re-create dashappp
    app = dash.Dash(**buffer['config'])

    # apply attributes
    for key, value in buffer['attrs'].items():
        setattr(app, key, value)

    # register callbacks
    cbregistry = buffer['rebuild'].get('cbregistry', {})
    for cid, cvalue in cbregistry.items():
        app.callback_map[cid] = {
            'inputs': cvalue['inputs'],
            'state': cvalue['state'],
            'callback': dill.loads(cvalue['callback'])
        }

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
