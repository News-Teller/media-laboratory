# Generic
from urllib.parse import urlparse
from typing import Optional

# Data handling
import pandas as pd

# Plotly's Dash
import dash
import dash_html_components as html

from .utils import generate_data_link, is_dataframe_large

# should also support dcc, not only html elements
dash_component_type = dash.development.base_component.ComponentMeta

NEWSTELLER_LOGO_URL = 'https://avatars.githubusercontent.com/u/54896707?s=48'

def generate_source_span(source: str) -> dash_component_type:
    """Generate the Dash component for the data source footer element.
    If `source` is a URL then an HTML anchor tag is created,
    otherwise will be just a text containing `source`.

    :param source: Source of the visualisation data
    :type source: str
    :return: Dash html.Span element
    :rtype: dash_component_type
    """
    display_name, href = source, None

    try:
        url = urlparse(source)

        if url and url.netloc:
            display_name = url.netloc
            url = source

    except ValueError as error:
        print(error)

    if href:
        return html.Span([
            'Source: ',
            html.A(display_name, href=href)
        ])
    else:
        return html.Span(f'Source: {display_name}')


def get_newsteller_layout(title: str, description: str, author: str, plot: dash_component_type,
    data_source: Optional[str] = None, dataframe: Optional[pd.DataFrame] = None) -> dash_component_type:
    """Wraps the `plot` in a branded NewsTeller layout.

    :param title: visualisation's title which will appear in the HTML title tag
    :type title: str
    :param description: brief description which will appear in the HTML description metatag
    :type description: str
    :param author: author of the visualisation
    :type author: str
    :param plot: leading visualisation
    :type plot: dash_component_type
    :param data_source: data source, defaults to None
    :type data_source: Optional[str], optional
    :param dataframe: leading visualisation's data, defaults to None
    :type dataframe: Optional[pd.DataFrame], optional
    :return: a dash component that can be set as app.layout
    :rtype: dash_component_type
    """

    # header
    header = html.Div(children=[
        html.H1(title),
        html.P(description)
    ], className='header')

    # footer
    footer_ul_elements = [
        html.Li(children=[html.Span(f'Author: {author}')])
    ]

    if data_source:
        footer_ul_elements.append(
            html.Li(generate_source_span(data_source))
        )

    if dataframe is not None:
        href = generate_data_link(dataframe)
        footer_ul_elements.append(html.Li(
            html.Span(html.A('Get the data', href=href, download=f'data.csv'))
        ))

    footer_left = html.Div(children=[html.Ul(children=footer_ul_elements)], className='footer-left')

    # Include logo as remote URL to reduce layout size
    footer_right = html.Div(children=[
            html.Img(src=NEWSTELLER_LOGO_URL, alt='newsteller-logo', className='logo'),
            html.Strong('NewsTeller'),
    ], className='footer-right')

    footer = html.Div(children=[
            footer_left,
            footer_right,
    ], className='footer')

    return html.Div([header, plot, footer])

