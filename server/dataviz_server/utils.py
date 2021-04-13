import re
from typing import Optional, List
import flask


VIZ_RECORD_REQUIRED_KEYS = ['uid', 'title', 'createdAt', 'tags']

def parse_tags(tags_parameter: str, allowed_pattern: Optional[re.Pattern] = None) -> list:
    """Parse the `tags` query parameter.

    :param tags_parameter: tags parameter
    :type tags_parameter: str
    :param allowed_pattern: Allow only tags that match this regex, defaults to None
    :type allowed_pattern: Optional[re.Pattern], optional
    :return: A list of tags
    :rtype: list
    """
    tags = tags_parameter.split(',') if tags_parameter else []

    if allowed_pattern:
        tags = [tag for tag in tags if re.match(allowed_pattern, tag)]

    return tags

def build_list_query(tags: list) -> dict:
    """Build the query to list visualizations.

    :param tags: List of tags. Can be empty.
    :type tags: list
    :return: MongoDB find query.
    :rtype: dict
    """
    return {'tags': { '$all': tags }} if tags else {}

def parse_viz_records(records: List[dict]) -> Optional[dict]:
    """Simple utility to extract a subset of info from the vizs db records.
    Used to avoid displaying all the viz info from the API.

    :param records: Viz database results.
    :type records: List[dict]
    :return: List of Viz's uid, title, creation date, tags.
    :rtype: Optional[dict]
    """
    if not records:
        return []

    data = list()

    for record in records:
        try:
            data.append({
                'uid': record['uid'],
                'title': record['title'],
                'createdAt': record['createdAt'],
                'updatedAt': record['updatedAt'],
                'tags': record['tags'] if 'tags' in record else [],
            })

        except KeyError:
            pass

    return data
