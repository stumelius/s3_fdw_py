import logging
import pytest
import boto3
import multicorn.utils
from unittest.mock import patch
from s3_fdw import S3ForeignDataWrapper

VALID_OPTIONS = {
    'object_name': 'pytest.csv',
    'bucket_name': 'pytest',
    'access_key': 'pytest123',
    'secret_key': 'pytest123',
    'endpoint_url': 'http://localhost:9000',
}


def get_keys(*args):
    return {key: VALID_OPTIONS[key] for key in args}


def test_s3_fdw_creates_attributes_from_options_keys_and_stores_columns_list():
    options = VALID_OPTIONS
    columns = ['a', 'b', 'c']
    s3_fdw = S3ForeignDataWrapper(options=VALID_OPTIONS, columns=columns)
    for key, value in options.items():
        assert getattr(s3_fdw, key) == value
    assert s3_fdw.columns == columns


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
def test_s3_fdw_logs_error_to_postgres_if_required_option_is_missing(
    log_to_postgres, options, error_messages
):
    s3_fdw = S3ForeignDataWrapper(options=options, columns=[])
    assert log_to_postgres.call_count == len(error_messages)
    for error_message in error_messages:
        log_to_postgres.assert_any_call(error_message, logging.ERROR)


def test_s3_fdw_endpoint_url_is_set_to_none_if_not_specified_in_options():
    options = {
        key: value for key, value in VALID_OPTIONS.items() if key != 'endpoint_url'
    }
    s3_fdw = S3ForeignDataWrapper(options=options, columns=[])
    assert s3_fdw.endpoint_url is None


def test_s3_fdw_execute_infers_csv_delimiter_and_yields_rows(s3_fixture):
    options = VALID_OPTIONS
    s3_bucket = s3_fixture.Bucket('pytest')
    data = b'a,b,c\n1,2,3'
    object_name = options['object_name']
    s3_object = s3_bucket.put_object(Body=data, Key=object_name)
    s3_fdw = S3ForeignDataWrapper(options=options, columns=['a', 'b', 'c'])
    rows = list(s3_fdw.execute(quals={}, columns={}))
    assert len(rows) == 1
    assert rows[0] == [1, 2, 3]
