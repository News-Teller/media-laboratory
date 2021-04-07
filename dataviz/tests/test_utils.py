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


def test_check_app_factory():
    def real_create_app_dash():
        app = utils.Dash('test')

        return app

    def real_create_app_jupyterdash():
        app = utils.JupyterDash('test')

        return app

    def fake_create_app():
        return 1

    assert utils.app_factory_checker(real_create_app_dash)
    assert utils.app_factory_checker(real_create_app_jupyterdash)
    assert not utils.app_factory_checker(fake_create_app)
