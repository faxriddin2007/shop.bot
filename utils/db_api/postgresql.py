import psycopg2
from data.config import DB_PASS, DB_HOST, DB_NAME, DB_PORT, DB_USER

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        self.cursor = self.conn.cursor()

    def get_user(self, chat_id):
        query = f"SELECT * FROM users WHERE chat_id={chat_id}"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_user_all_products(self, chat_id: int):
        query = f"SELECT * FROM products WHERE status = 'active' AND chat_id = {chat_id}"
        products = self.cursor.execute(query).fetchall()
        return products

    def get_all_products(self):
        query = "SELECT * FROM products WHERE status = 'active'"
        products = self.cursor.execute(query).fetchall()
        return products

    def delete_products(self, product_id: int):
        query = f"delete from products where id={product_id}"
        delete = self.cursor.execute(query)
        self.conn.commit()
        return delete

    def insert_user(self, data: dict):
        full_name = data['full_name']
        login = data['login']
        password = data['password']
        phone_number = data['phone_number']
        chat_id = data['chat_id']

        query = "INSERT INTO users (full_name, login, password, chat_id, phone_number) VALUES (%s,%s,%s,%s,%s)"
        values = (full_name, login, password, chat_id, phone_number)

        self.cursor.execute(query, values)
        self.conn.commit()
        return True

    def insert_product(self, data: dict):
        name = data['name']
        price = data['price']
        photo = data['photo']
        chat_id = data['chat_id']
        status = data['status']
        info = data['info']

        query = "INSERT INTO products (name, price, photo, chat_id, status, info) VALUES (%s,%s,%s,%s,%s, %s)"
        values = (name, price, photo, chat_id, status, info)

        self.cursor.execute(query, values)
        self.conn.commit()
        return True


class TableManager(DBManager):
    def create_table(self):
        query = """
CREATE TABLE IF NOT EXISTS users (
id SERIAL PRIMARY KEY,
phone_number TEXT NOT NULL,
login TEXT NOT NUll,
password TEXT NOT NULL,
full_name TEXT NOT NULL,
chat_id BIGINT
)
"""

#     def create_table(self):
#         query = """
# CREATE TABLE products (
# id SERIAL PRIMARY KEY,
# name TEXT NOT NULL,
# info TEXT NOT NULL,
# photo TEXT NOT NULL,
# price REAL NOT NUll,
# status TEXT,
# chat_id BIGINT
# )
# """

        self.cursor.execute(query)
        self.conn.commit()


db_manager = DBManager()
table_manager = TableManager()
table_manager.create_table()
