import pytest
import boto3
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_fdw import ForeignDataWrapper
from s3_fdw import S3ForeignDataWrapper


@pytest.fixture
@pytest.helpers.register
def options_fixture():
    return {
        'object_name': 'pytest.csv',
        'bucket_name': 'pytest',
        'access_key': 'pytest123',
        'secret_key': 'pytest123',
        'endpoint_url': 'http://localhost:9000',
    }


@pytest.fixture
def sqlalchemy_fdw_fixture(options_fixture):
    url = 'pgfdw://pytest:pytest@localhost:5432/pytest'
    engine = create_engine(url)
    with engine.connect() as con:
        try:
            con.execute('CREATE EXTENSION multicorn;')
        except ProgrammingError as e:
            pass
    metadata = MetaData(bind=engine)
    fdw = ForeignDataWrapper(
        's3_fdw_srv',
        'multicorn',
        metadata=metadata,
        options={
            'wrapper': 's3_fdw.{cls_name}'.format(
                cls_name=S3ForeignDataWrapper.__name__
            )
        },
    )
    fdw.create(checkfirst=True)
    yield fdw
    fdw.drop(checkfirst=True)


@pytest.fixture
def s3_fixture(options_fixture):
    s3 = boto3.resource(
        's3',
        endpoint_url=options_fixture['endpoint_url'],
        aws_access_key_id=options_fixture['access_key'],
        aws_secret_access_key=options_fixture['secret_key'],
    )
    bucket = s3.create_bucket(Bucket=options_fixture['bucket_name'])
    yield s3
    bucket.objects.all().delete()
    bucket.delete()
