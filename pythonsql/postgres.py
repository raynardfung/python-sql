import pg8000.native
import pandas as pd 

class Postgres():
    def __init__(self, host, database, user, password, port):
        self.host     = host
        self.database = database
        self.user     = user
        self.password = password
        self.port     = port

        self.pg8000_conn =self._create_pg8000_connection()

    
    def _create_pg8000_connection(self):
        return pg8000.native.Connection(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port
        )

    
    def execute_sql(self, statement):
        response = self.pg8000_conn.run(statement)
        if response is not None:
            list_of_rows = []
            for row in response:
                list_of_rows.append(row)
            
            return pd.DataFrame(list_of_rows)

        return pd.DataFrame() # Return an empty Dataframe if the response was empty


    def _df_to_list(self, df, colnum=0):
        lis = list(df.iloc[:,colnum])
        lis.sort()

        return lis


    def list_schemas(self):
        statement = """
        select distinct schema_name
        from information_schema.schemata
        """

        df = self.execute_sql(statement)
        lis = self._df_to_list(df)

        return lis


    def list_tables(self, schema):
        statement = """
        select distinct tablename
        from pg_tables
        where 1=1
        and schemaname = '{schema}'
        """.format(schema=schema)

        df = self.execute_sql(statement)
        lis = self._df_to_list(df)

        return lis


    def list_groups(self):
        statement = """
        select distinct groname
        from pg_group
        """

        df = self.execute_sql(statement)
        lis = self._df_to_list(df)

        return lis


    def list_users(self):
        statement = """
        select distinct usename
        from pg_user
        """

        df = self.execute_sql(statement)
        lis = self._df_to_list(df)

        return lis


    def _exists_boolean(self, exists): # Converts the SQL response ("true" or "false" string) to boolean
        exists = list(exists.iloc[:,0])
        return bool(exists[0])


    def schema_exists(self, schema):
        statement = """
        select exists (
            select schema_name
            from information_schema.schemata
            where schema_name = '{schema}'
        );
        """.format(schema=schema)

        return self._exists_boolean( self.execute_sql(statement) )


    def table_exists(self, schema, table):
        statement = """
        select exists (
            select * 
            from pg_tables
            where 1=1
            and schemaname = '{schema}'
            and tablename = '{table}'
        );
        """.format(schema=schema, table=table)

        return self._exists_boolean( self.execute_sql(statement) )


    def group_exists(self, group):
        statement = """
        select exists (
            select distinct groname
            from pg_group
            where groname = '{group}'
        );
        """.format(group=group)

        return self._exists_boolean( self.execute_sql(statement) )


    def user_exists(self, user):
        statement = """
        select exists (
            select distinct usename
            from pg_user
            where usename = '{user}'
        );
        """.format(user=user)

        return self._exists_boolean( self.execute_sql(statement) )


    def table_empty(self, schema, table):
        statement = """
        select *
        from {schema}.{table}
        limit 1
        """.format(schema=schema, table=table)

        df = self.execute_sql(statement)
        return df.empty


    def get_table_disk_size(self, schema, table): # Returns the disk size of a given table in a pretty string format, using kB, MB, GB or TB as appropriate
        statement = """
        select pg_size_pretty (
            pg_total_relation_size('"{schema}"."{table}"')
        );
        """.format(schema=schema, table=table)

        df = self.execute_sql(statement)

        return df.iloc[0,0]
        