# Generic
from urllib.parse import quote

# Data handling
import pandas as pd

def generate_data_link(df: pd.DataFrame) -> str:
    """Serialise data in order to make it downloadable from a HTML anchor tag.
    The returned content needs to be placed inside the href attribute.

    :param df: Data
    :type df: pd.DataFrame
    :return: serialise data
    :rtype: str
    """
    # Don't serve large dataset
    if is_dataframe_large(df):
        return ''

    csv_string = df.to_csv(encoding='utf-8', index=False)
    return 'data:application/octet-stream;charset=utf-8,' + quote(csv_string)

def is_dataframe_large(df: pd.DataFrame) -> bool:
    """Determines if a pandas DataFrame can be declared as large.

    :param df: Data
    :type df: pd.DataFrame
    :return: `True` if data is large, `False` otherwise
    :rtype: bool
    """
    return df.empty or df.shape[0] >= 15000
