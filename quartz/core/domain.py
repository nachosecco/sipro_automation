import os
from mysql.connector import connect, Error

class Domain:
    def __init__(self):
        self.user = os.environ.get('QRT_DOMAIN_DB_USER')
        self.password = os.environ.get('QRT_DOMAIN_DB_PASSWORD')
        self.host = os.environ.get('QRT_DOMAIN_DB_HOST', 'localhost')
        self.port = int(os.environ.get('QRT_DOMAIN_DB_PORT', 3306))
        self.db = 'domain'
        try:
            self.connection = connect(
                host=self.host,
                port=self.port,
                database=self.db,
                user=self.user,
                password=self.password,
                ssl_disabled=True
            )
            print(self.connection)
        except Error as e:
            print(e)

    def retrieve(self, sql):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def execute(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            self.connection.commit()
