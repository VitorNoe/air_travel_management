from src.database import Database
from hashlib import sha256

class Auth:
    def __init__(self):
        self.db = Database()

    def login(self, username, password):
        hashed_password = sha256(password.encode()).hexdigest()
        query = "SELECT access_level FROM users WHERE username = %s AND password_hash = %s"
        result = self.db.fetch_data(query, (username, hashed_password))
        return result[0][0] if result else None