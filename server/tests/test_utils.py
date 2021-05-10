import pytest

from dataviz_server.utils import (parse_tags, build_list_query,
    parse_viz_records, get_logger, VIZ_RECORD_REQUIRED_KEYS)
from dataviz_server.utils import re


FAKE_VIZ_RECORD = {key:key for key in VIZ_RECORD_REQUIRED_KEYS}
FAKE_VIZ_RECORD['tags'] = ['tags']
FAKE_VIZ_RECORD_PLUS = FAKE_VIZ_RECORD.copy()
FAKE_VIZ_RECORD_PLUS['randomkey'] = 'randomkey'

@pytest.mark.parametrize(
    'req, pattern, expected',
    [
        # w/o regex pattern
        ('', None, []),
        ('tag1,tag2', None, ['tag1', 'tag2']),
        # w/ regex pattern
        ('', '^[a-zA-Z]+$', []),
        ('tag1,tag2', '^[a-zA-Z]+$', []),
    ],
)
def test_parse_tags(req, pattern, expected):
    compiled = re.compile(pattern) if pattern else None
    assert parse_tags(req, compiled) == expected


@pytest.mark.parametrize(
    'req, expected',
    [
        ([], {}),
        (['tag1', 'tag2'], {'tags': { '$all': ['tag1', 'tag2'] }})
    ],
)
def test_build_list_query(req, expected):
    assert build_list_query(req) == expected


@pytest.mark.parametrize(
    'req, expected',
    [
        (None, []),
        ([], []),
        ([FAKE_VIZ_RECORD], [FAKE_VIZ_RECORD]),
        ([FAKE_VIZ_RECORD_PLUS], [FAKE_VIZ_RECORD])
    ],
)
def test_parse_viz_records(req, expected):
    assert parse_viz_records(req) == expected


def test_get_logger():
    logger = get_logger()

    assert logger
