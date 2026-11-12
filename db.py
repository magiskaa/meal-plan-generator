import sqlite3

class database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.db_file = "database.db"

    def init_db(self):
        table_foods = """
            CREATE TABLE IF NOT EXISTS foods (
                id INTEGER PRIMARY KEY, 
                name text NOT NULL, 
                days_between INTEGER NOT NULL, 
                last_date text
            );
        """
        table_ingredients = """
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER, 
                name text NOT NULL,
                FOREIGN KEY (id)
                    REFERENCES foods (id)
            );
        """

        try:
            self.conn = sqlite3.connect(self.db_file)
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
            self.conn.execute("PRAGMA foreign_keys = ON")
            
            self.cursor = self.conn.cursor()
            self.cursor.execute(table_foods)
            self.cursor.execute(table_ingredients)
            self.conn.commit()

        except sqlite3.OperationalError as e:
            print("Failed to open database: ", e)
        except Exception as e:
            print("Unkown error occurred: ", e)

    def close_db(self):
        self.conn.close()

    def add_food(self, name, days_between, last_date=None):
        sql = """ 
            INSERT INTO foods(name,days_between,last_date)
            VALUES(?,?,?)
        """
        self.cursor.execute(sql, (name, days_between, last_date))
        self.conn.commit()

        return self.cursor.lastrowid

    def update_food(self, last_date, food_id):
        sql = """ 
            UPDATE foods
            SET last_date = ?
            WHERE id = ?
        """
        self.cursor.execute(sql, (last_date, food_id))
        self.conn.commit()

    def get_foods(self):
        sql = """
            SELECT * FROM foods
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def add_ingredient(self, food_id, name):
        sql = """ 
            INSERT INTO ingredients(id,name)
            VALUES(?,?)
        """
        self.cursor.execute(sql, (food_id, name))
        self.conn.commit()

    def get_ingredients(self, food_id):
        sql = """
            SELECT name FROM ingredients
            WHERE id = ?
        """
        self.cursor.execute(sql, (food_id,))
        return self.cursor.fetchall()
