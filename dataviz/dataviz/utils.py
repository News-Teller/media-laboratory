from typing import Any
from uuid import uuid4


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
