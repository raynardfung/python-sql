import pytest
from pythonsql import postgres 

@pytest.fixture
def pg():
    # Create a connection to a public Postgres database (https://rnacentral.org/help/public-database)
    return postgres.Postgres(
        host='hh-pgsql-public.ebi.ac.uk',
        database='pfmegrnargs',
        user='reader',
        password='NWDMCE5xdipIjRrp',
        port=5432
    )


def test_execute_sql(pg):
    statement = """
    select * from rnc_database
    """
    df = pg.execute_sql(statement)
    assert df.empty == False


def test_list_schemas(pg):
    schema_list = pg.list_schemas()
    assert schema_list == ['information_schema', 'pg_catalog', 'rnacen']


def test_list_tables(pg):
    table_list = pg.list_tables('information_schema')
    assert table_list == ['sql_features', 'sql_implementation_info', 'sql_languages', 'sql_packages', 'sql_parts', 'sql_sizing', 'sql_sizing_profiles']


def test_list_groups(pg):
    group_list = pg.list_groups()
    assert group_list == ['pg_monitor', 'pg_read_all_settings', 'pg_read_all_stats', 'pg_signal_backend', 'pg_stat_scan_tables']


def test_list_users(pg):
    user_list = pg.list_users()
    assert user_list == ['hag', 'nagios', 'postgres', 'reader', 'rnacen', 'wpk8pub']


def test_schema_exists(pg):
    assert pg.schema_exists('rnacen') == True


def test_table_exists(pg):
    assert pg.table_exists('rnacen', 'rna') == True


def test_group_exists(pg):
    assert pg.group_exists('pg_read_all_stats') == True


def test_user_exists(pg):
    assert pg.user_exists('postgres') == True


def test_table_empty(pg):
    assert pg.table_empty('rnacen', 'rna') == False