import pytest
import mock
import datetime

from dataviz.dataviz import DataViz, DataVizException
from dataviz.dataviz import os, pymongo, dill, bson, ConnectionFailure
from dataviz.serializer import dashapp_serializer, dashapp_deserializer
from tests.assets.simple_app import app as simple_app


FAKE_USER = 'test'
FAKE_DB_RECORD = {
    '_id': 'test',
    'uid': 'test',
    'title': 'test',
    'user': 'test',
    'dashapp': dashapp_serializer(simple_app),
    'dashapp_prev': None,
    'createdAt': datetime.datetime(2021, 1, 1, 0, 0, 0, 0),
    'updatedAt': datetime.datetime(2021, 1, 1, 0, 0, 0, 0),
    'locked': False,
    'tags': ['test'],
}
FAKE_DB_RESULT = FAKE_DB_RECORD.copy()
FAKE_DB_RESULT['dashapp'] = dashapp_deserializer(FAKE_DB_RECORD['dashapp'])
FAKE_VIZ_PARAMS = {k:FAKE_DB_RESULT[k] for k  in ['uid', 'title', 'tags']}
FAKE_VIZ_PARAMS['dash_app'] = simple_app


@mock.patch.dict(os.environ, {'DB_USER': ''})
def test_no_user():
    with pytest.raises(ValueError) as excinfo:
       DataViz()

    assert type(excinfo.value) is ValueError
    assert str(excinfo.value) == 'User not provided!'


@pytest.mark.parametrize(
    'params, exception, message',
    [
        ({'uid': 'bad-uid!!', 'title': FAKE_VIZ_PARAMS['title'], 'dash_app': FAKE_VIZ_PARAMS['dash_app']}, ValueError, ''),
        ({'uid': FAKE_VIZ_PARAMS['uid'], 'title': FAKE_VIZ_PARAMS['title'], 'dash_app': None}, ValueError, 'Missing parameter'),
    ],
)
def test_store_raise(mocker, params, exception, message):
    with pytest.raises(exception) as excinfo:
       dv = DataViz(user=FAKE_USER)
       dv.store(**params)

    assert type(excinfo.value) is exception

    if message:
        assert str(excinfo.value) == message


def test_store_new_app(mocker):
    mocker.patch('pymongo.collection.Collection.find_one', return_value=dict())
    mocker.patch('pymongo.collection.Collection.update_one', return_value=True)

    dv = DataViz(user=FAKE_USER)
    res = dv.store(**FAKE_VIZ_PARAMS)

    assert res
    # assert mock_update_one.call_args == ...


def test_store_update_app_different_user(mocker):
    mock_find_one = mocker.patch('pymongo.collection.Collection.find_one')
    mock_find_one.return_value = {
        'uid':FAKE_VIZ_PARAMS['uid'],
        'title':FAKE_VIZ_PARAMS['title'],
        'user': 'test2'
    }

    dv = DataViz(user=FAKE_USER)
    with pytest.raises(ValueError) as excinfo:
        dv.store(**FAKE_VIZ_PARAMS)

    assert type(excinfo.value) is ValueError
    assert str(excinfo.value) == f"Viz '{FAKE_VIZ_PARAMS['uid']}' already exists!"


def test_store_update_app_same_user_app_locked(mocker):
    mock_find_one = mocker.patch('pymongo.collection.Collection.find_one')
    locked_viz = FAKE_DB_RECORD.copy()
    locked_viz['locked'] = True
    mock_find_one.return_value = locked_viz

    dv = DataViz(user=FAKE_USER)
    with pytest.raises(DataVizException) as excinfo:
        dv.store(**FAKE_VIZ_PARAMS)

    assert type(excinfo.value) is DataVizException
    assert str(excinfo.value) == 'This viz is locked!'


def test_store_update_app_same_user_app_unlocked(mocker):
    mocker.patch('pymongo.collection.Collection.find_one', return_value=FAKE_DB_RECORD)
    mocker.patch('pymongo.collection.Collection.update_one', return_value=True)

    dv = DataViz(user=FAKE_USER)
    assert dv.store(**FAKE_VIZ_PARAMS)

    # assert mock_update_one.assert_called_with(..)


@pytest.mark.parametrize('record', [dict(), FAKE_DB_RECORD])
def test_load(mocker, record):
    mocker.patch('pymongo.collection.Collection.find_one', return_value=record)

    dv = DataViz(user=FAKE_USER)
    res = dv.load(uid=FAKE_VIZ_PARAMS['uid'])

    if record:
        assert ('_id' not in res) and ('user' not in res)
        assert 'dashapp' in res
    else:
        assert res is None


def test_delete_no_record(mocker):
    mocker.patch('pymongo.collection.Collection.find_one', return_value=dict())

    dv = DataViz(user=FAKE_USER)
    res = dv.load(uid=FAKE_VIZ_PARAMS['uid'])

    assert not res


@pytest.mark.parametrize(
    'user_input, expected',
    [
        ('wrong_input', False),
        ('yes', True)
    ]
)
def test_delete_confirm_input(mocker, user_input, expected):
    mocker.patch('builtins.input', return_value=user_input)
    mocker.patch('pymongo.collection.Collection.find_one', return_value=FAKE_DB_RECORD)

    mock_delete_one = mocker.patch('pymongo.collection.Collection.delete_one', return_value=True)

    dv = DataViz(user=FAKE_USER)
    res = dv.delete(uid=FAKE_VIZ_PARAMS['uid'], ask_confirm=True)

    assert res == expected

    if user_input == 'yes':
        assert mock_delete_one.call_args == mock.call(
            {'uid': FAKE_VIZ_PARAMS['uid'], 'user': FAKE_USER
        })


def test_delete_wo_confirm(mocker):
    mocker.patch('pymongo.collection.Collection.find_one', return_value=FAKE_DB_RECORD)
    mock_delete_one = mocker.patch('pymongo.collection.Collection.delete_one', return_value=True)

    dv = DataViz(user=FAKE_USER)
    res = dv.delete(uid=FAKE_VIZ_PARAMS['uid'], ask_confirm=False)

    assert res
    assert mock_delete_one.call_args == mock.call({'uid': FAKE_VIZ_PARAMS['uid'], 'user': FAKE_USER})

def test_delete_locked_viz(mocker):
    locked_record = FAKE_DB_RECORD.copy()
    locked_record['locked'] = True
    mocker.patch('pymongo.collection.Collection.find_one', return_value=locked_record)

    dv = DataViz(user=FAKE_USER)

    with pytest.raises(DataVizException) as excinfo:
        dv.delete(uid=FAKE_VIZ_PARAMS['uid'], ask_confirm=False)

    assert type(excinfo.value) is DataVizException
    assert str(excinfo.value) == 'This viz is locked!'

@pytest.mark.parametrize(
    'record, expected',
    [
        (None, False),
        (FAKE_DB_RECORD, True)
    ]
)
def test_lock(mocker, record, expected):
    mock_find_one = mocker.patch('pymongo.collection.Collection.find_one', return_value=record)
    mock_update_one = mocker.patch('pymongo.collection.Collection.update_one', return_value=True)

    dv = DataViz(user=FAKE_USER)
    res = dv.lock(uid=FAKE_VIZ_PARAMS['uid'])

    call_params = {'uid': FAKE_VIZ_PARAMS['uid'], 'user': FAKE_USER}

    assert res == expected
    assert mock_find_one.call_args == mock.call(call_params)

    if record:
        assert mock_update_one.call_args == mock.call(
            call_params, {'$set': {'locked': True}}, upsert=False
        )

@pytest.mark.parametrize(
    'record, expected',
    [
        (None, False),
        ({**FAKE_DB_RECORD, **{'locked': True}}, True)
    ]
)
def test_unlock(mocker, record, expected):
    mock_find_one = mocker.patch('pymongo.collection.Collection.find_one', return_value=record)
    mock_update_one = mocker.patch('pymongo.collection.Collection.update_one', return_value=True)

    dv = DataViz(user=FAKE_USER)
    res = dv.unlock(uid=FAKE_VIZ_PARAMS['uid'])

    call_params = {'uid': FAKE_VIZ_PARAMS['uid'], 'user': FAKE_USER}

    assert res == expected
    assert mock_find_one.call_args == mock.call(call_params)

    if record:
        assert mock_update_one.call_args == mock.call(
            call_params, {'$set': {'locked': False}}, upsert=False
        )


@pytest.mark.parametrize(
    'req, expected',
    [
        ({}, True),
        (FAKE_DB_RECORD, False),
    ],
)
def test_check_uid_availability(mocker, req, expected):
    mock_find_one = mocker.patch('pymongo.collection.Collection.find_one')
    mock_find_one.return_value = req

    dv = DataViz(user=FAKE_USER)
    res = dv.check_uid_availability(uid=FAKE_VIZ_PARAMS['uid'])

    assert mock_find_one.call_args == mock.call({'uid': FAKE_VIZ_PARAMS['uid']})
    assert res == expected


@pytest.mark.parametrize(
    'side_effect, expected',
    [
        (ConnectionFailure(), False),
        (None, True),
    ],
)
def test_is_db_connected(mocker, side_effect, expected):
    mocker.patch('pymongo.database.Database.command', side_effect=side_effect)

    dv = DataViz(user=FAKE_USER)
    res = dv.is_db_connected()

    assert res == expected


@pytest.mark.parametrize(
    'records, expected',
    [
        ([], []),
        ([FAKE_DB_RECORD], [FAKE_DB_RESULT]),
    ],
)
def test_get_my_visualisations(mocker, records, expected):
    mock_find_one = mocker.patch('pymongo.collection.Collection.find_one', return_value=records)

    dv = DataViz(user=FAKE_USER)
    res = dv.get_my_visualisations()

    assert mock_find_one.call_args == mock.call({'user': FAKE_USER})

    for record in res:
        assert '_id' not in record
        assert 'dashapp' in record

@pytest.mark.parametrize(
    'record, expected',
    [
        (None, None),
        (dict(), dict()),
        (FAKE_DB_RECORD, FAKE_DB_RESULT),
    ],
)
def test_clean_record(mocker, record, expected):
    dv = DataViz(user=FAKE_USER)
    res = dv._clean_record(record)

    if res:
        for record in res:
            assert ('_id' not in record) and ('user' not in record)
            assert 'dashapp' in res

    else:
        assert res == expected
