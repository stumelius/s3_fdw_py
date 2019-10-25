def test_sqlalchemy_fdw_fixture_creates_fdw_server(sqlalchemy_fdw_fixture):
    with sqlalchemy_fdw_fixture.metadata.bind.connect() as con:
        rows = list(
            con.execute(
                """
            select 
                srvname as name, 
                srvowner::regrole as owner, 
                fdwname as wrapper, 
                srvoptions as options
            from pg_foreign_server
            join pg_foreign_data_wrapper w on w.oid = srvfdw;
            """
            )
        )
        assert len(rows) == 1
        server_name = rows[0][0]
        assert server_name == sqlalchemy_fdw_fixture.name


def test_s3_fixture_creates_pytest_bucket(s3_fixture):
    buckets = list(s3_fixture.buckets.all())
    assert len(buckets) == 1
    assert buckets[0].name == 'pytest'
