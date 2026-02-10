import psycopg2
from settings import DB_NAME, DB_USER


class Database:
    def __init__(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
            )
            self.conn.autocommit = True
        except Exception as e:
            print(f"Database connection failed: {e}")
            self.conn = None

    def get_codename(self, player_id):
        if self.conn is None:
            return None
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT codename FROM players WHERE id = %s", (player_id,))
            row = cursor.fetchone()
            cursor.close()
            return row[0] if row else None
        except Exception as e:
            print(f"DB query error: {e}")
            return None

    def insert_player(self, player_id, codename):
        if self.conn is None:
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO players (id, codename) VALUES (%s, %s)",
                (player_id, codename),
            )
            cursor.close()
            return True
        except Exception as e:
            print(f"DB insert error: {e}")
            return False

    def close(self):
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
