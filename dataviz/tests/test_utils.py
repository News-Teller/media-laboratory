import re
import pytest

import dataviz.utils as utils


def test_uid_len():
    uid = utils.generate_uid()

    assert len(uid) == 12


def test_uid_pattern():
    pattern = re.compile('^[a-zA-Z0-9]+$')
    uid = utils.generate_uid()

    assert re.match(pattern, uid)

