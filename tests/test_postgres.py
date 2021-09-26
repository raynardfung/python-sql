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