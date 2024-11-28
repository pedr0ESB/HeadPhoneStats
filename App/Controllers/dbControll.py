import psycopg2

class DatabaseConnection:
    def __init__(self, host, dbname, user, password, port):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port

    def query_data(self, query):
        """Executa consultas no banco de dados e retorna os resultados."""
        try:
            connection = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )

            rec = connection.cursor()
            rec.execute(query)
            result = rec.fetchall()
            rec.close()
            return result   

        except psycopg2.Error as e:
            raise Exception(f"Error executing query: {e}")


    def insert_data(self, query):
        """Executa comandos de inserção no banco de dados."""
        try:
            connection = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )

            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            cur.close()

        except psycopg2.Error as e:
            connection.rollback()
            raise Exception(f"Error executing insert: {e}")