import pytest
import boto3
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_fdw import ForeignDataWrapper


@pytest.fixture
def fdw_fixture():
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
        options={'wrapper': 's3_fdw.S3Fdw'},
    )
    fdw.create(checkfirst=True)
    yield fdw
    fdw.drop(checkfirst=True)


@pytest.fixture
def s3_fixture():
    s3 = boto3.resource(
        's3',
        endpoint_url='http://localhost:9000',
        aws_access_key_id='pytest123',
        aws_secret_access_key='pytest123',
    )
    bucket = s3.create_bucket(Bucket='pytest')
    yield s3
    bucket.objects.all().delete()
    bucket.delete()
