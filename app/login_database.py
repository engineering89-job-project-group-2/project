from passlib.handlers.sha2_crypt import sha256_crypt
from passlib.hash import pbkdf2_sha256
import sqlite3


def encrypt(password):
    password = sha256_crypt.hash(password)
    return password


class LoginDatabase:

    # Connect to the database
    users_db = sqlite3.connect('app/databases/users.db', check_same_thread=False)
    users_db_cursor = users_db.cursor()

    def database_initialise(self):
        self.users_db_cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            staff_id integer,
            username text,
            password text,
            role text
        )""")
        return "Completed"

    def new_user(self, staff_id, username, password, role):
        password_encrypted = pbkdf2_sha256.hash(password)
        self.users_db_cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (staff_id, username, password_encrypted, role))
        self.users_db.commit()
        return True

    def compare(self, username, password):
        try:
            self.users_db_cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            password_hash = ' '.join(self.users_db_cursor.fetchone()) # Removes the hash from a tuple as sql exports info as a tuple
            password = pbkdf2_sha256.verify(password, password_hash)
            return True if password else False
        except Exception as e:
            print(e)
            return False