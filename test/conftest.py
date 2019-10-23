import pytest
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
    fdw = ForeignDataWrapper('s3_fdw_srv', 'multicorn', metadata=metadata, options={'wrapper': 's3_fdw.S3Fdw'})
    fdw.create(checkfirst=True)
    yield fdw
    fdw.drop(checkfirst=True)