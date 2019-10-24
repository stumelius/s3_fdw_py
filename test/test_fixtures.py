def test_fdw_fixture_creates_fdw_server(fdw_fixture):
    with fdw_fixture.metadata.bind.connect() as con:
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
        assert server_name == fdw_fixture.name
