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


    