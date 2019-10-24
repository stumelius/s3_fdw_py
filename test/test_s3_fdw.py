import logging
import multicorn.utils
from unittest.mock import patch
from s3_fdw import S3ForeignDataWrapper


def test_s3_fdw_parses_object_name_from_options():
    s3_fdw = S3ForeignDataWrapper(options={'object_name': 'pytest'}, columns={})
    assert s3_fdw.object_name == 'pytest'


@patch('multicorn.utils.log_to_postgres')
def test_s3_fdw_logs_error_to_postgres_if_no_object_name_in_options(log_to_postgres):
    s3_fdw = S3ForeignDataWrapper(options={}, columns={})
    log_to_postgres.assert_called_once_with('object_name required', logging.ERROR)
