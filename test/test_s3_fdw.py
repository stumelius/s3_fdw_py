import logging
import pytest
import multicorn.utils
from unittest.mock import patch
from s3_fdw import S3ForeignDataWrapper

VALID_OPTIONS = {
    'object_name': 'pytest.csv',
    'bucket_name': 'pytest',
    'access_key': 'pytest-access',
    'secret_key': 'pytest-secret',
}


def get_keys(*args):
    return {key: VALID_OPTIONS[key] for key in args}


def test_s3_fdw_creates_attributes_from_options_keys():
    options = VALID_OPTIONS
    s3_fdw = S3ForeignDataWrapper(options=VALID_OPTIONS, columns={})
    for key, value in options.items():
        assert getattr(s3_fdw, key) == value


@patch('multicorn.utils.log_to_postgres')
@pytest.mark.parametrize(
    'options,error_messages',
    [
        (
            {},
            [
                'object_name required',
                'bucket_name required',
                'access_key required',
                'secret_key required',
            ],
        ),
        (
            get_keys('object_name'),
            ['bucket_name required', 'access_key required', 'secret_key required'],
        ),
        (
            get_keys('object_name', 'bucket_name'),
            ['access_key required', 'secret_key required'],
        ),
        (get_keys('object_name', 'bucket_name', 'access_key'), ['secret_key required']),
        (get_keys('object_name', 'bucket_name', 'access_key', 'secret_key'), []),
    ],
)
def test_s3_fdw_logs_error_to_postgres_if_invalid_options(
    log_to_postgres, options, error_messages
):
    s3_fdw = S3ForeignDataWrapper(options=options, columns={})
    assert log_to_postgres.call_count == len(error_messages)
    for error_message in error_messages:
        log_to_postgres.assert_any_call(error_message, logging.ERROR)
