# Generic
from urllib.parse import quote
from uuid import uuid4

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

def generate_uid():
    """Generate a 12-char uuid (universally unique identifier).

    :return: uuid
    :rtype: str
    """
    # Note: from our tests, we experienced 0 collision in 1M draws of 12-char uuids
    uuid_str = str(uuid4())
    return uuid_str[:8] + uuid_str[9:13]

def is_documented_by(original):
  def wrapper(target):
    target.__doc__ = original.__doc__
    return target
  return wrapper
