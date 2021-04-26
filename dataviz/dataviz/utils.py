from typing import Any,  IO, Union
from uuid import uuid4
import six
from plotly.io import to_html


def generate_uid() -> str:
    """Generate a 12-char uuid (universally unique identifier).

    :return: uuid
    :rtype: str
    """
    # Note: from our tests, we experienced 0 collision in 1M draws of 12-char uuids
    uuid_str = str(uuid4())
    return uuid_str[:8] + uuid_str[9:13]

def _is_function(obj: Any) -> bool:
    return hasattr(obj, '__call__')

def fig_to_html(
    fig: Union[object, dict],
    file: Union[str, IO],
    title: str = None,
    config: dict = None,
    html: str = None
) -> None:
    """Write a Plotly.js figure to an HTML file representation.
    Wrapper to the default Plotly.js `to_html` function.

    :param fig: Figure object or dict representing a figure
    :type fig: Union[object, dict]
    :param file: A string representing a local file path or a writeable object
    :type file: Union[str, IO]
    :param title: HTML page title, defaults to None
    :type title: str, optional
    :param config: Plotly.js figure config options, defaults to None
    :type config: dict, optional
    :param html: Override the standard html code, defaults to None
    :type html: str, optional
    """
    base_html = html or '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>{title}</title>
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="robots" content="noindex, nofollow">
        </head>
        <body>
            {div_fig}
        </body>
    </html>
    '''

    # Hide modebar
    config = config or {'displayModeBar': False}

    # Call Plotly.js function
    div_fig = to_html(
        fig=fig,
        config=config,
        include_plotlyjs='cdn',
        full_html=False
    )

    html_str = base_html.format(title=title, div_fig=div_fig)

    # Check if file is a string
    file_is_str = isinstance(file, six.string_types)

    # Write HTML string
    if file_is_str:
        with open(file, 'w') as f:
            f.write(html_str)
    else:
        file.write(html_str)
