import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connect()
        return cls._instance

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            print("Conexão com o banco de dados estabelecida!")
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor
        except Error as e:
            print(f"Erro na query: {e}")
            return None

    def fetch_data(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"Erro ao buscar dados: {e}")
            return []