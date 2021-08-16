import re
import pytest

import dataviz.utils as utils
from tests.assets.simple_app import figure


def test_uid_len():
    uid = utils.generate_uid()

    assert len(uid) == 12


def test_uid_pattern():
    pattern = re.compile('^[a-zA-Z0-9]+$')
    uid = utils.generate_uid()

    assert re.match(pattern, uid)


def test_fig_to_html(tmpdir):
    file = tmpdir.mkdir('fig_to_html').join('export.html')

    utils.fig_to_html(figure, file.strpath, title='Test')

    # assert a file has been written
    assert len(tmpdir.listdir()) == 1
