import psycopg2


class ConnectDB:
    '''Создает экземпляр класса для подключения к БД PostgresSQL'''

    def __init__(self, host: str, user: str, password: str, database: str, port: str) -> None:
        self.connect = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        self.connect.autocommit = True
