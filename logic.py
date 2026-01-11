import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    category TEXT,
                    instructions TEXT,
                    rating REAL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS ingredients (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS recipe_ingredients (
                    recipe_id INTEGER,
                    ingredient_id INTEGER,
                    quantity TEXT,
                    FOREIGN KEY(recipe_id) REFERENCES recipes(id),
                    FOREIGN KEY(ingredient_id) REFERENCES ingredients(id)
                )
            ''')
            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()

    def __select_data(self, sql, data=tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()

    def add_recipe(self, recipe_data):
        sql = 'INSERT INTO recipes (id, name, category, instructions, rating) VALUES (?, ?, ?, ?, ?)'
        self.__executemany(sql, [recipe_data])

    def add_ingredient(self, ingredient_data):
        sql = 'INSERT INTO ingredients (id, name) VALUES (?, ?)'
        self.__executemany(sql, [ingredient_data])

    def add_recipe_ingredient(self, recipe_ingredient_data):
        sql = 'INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES (?, ?, ?)'
        self.__executemany(sql, [recipe_ingredient_data])

    def get_all_recipes(self):
        sql = 'SELECT * FROM recipes'
        return self.__select_data(sql)

    def get_recipe_by_category(self, category):
        sql = 'SELECT * FROM recipes WHERE category = ?'
        return self.__select_data(sql, (category,))

    def get_ingredients_for_recipe(self, recipe_id):
        sql = '''
            SELECT i.name, ri.quantity
            FROM ingredients i
            INNER JOIN recipe_ingredients ri ON i.id = ri.ingredient_id
            WHERE ri.recipe_id = ?
        '''
        return self.__select_data(sql, (recipe_id,))
