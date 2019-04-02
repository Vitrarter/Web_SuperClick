import sqlite3


class DB:
    def __init__(self):
        conn = sqlite3.connect('news.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class NewsModel:
    def __init__(self, connection):
        self.connection = connection
        self.init_table()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(50),
                             content VARCHAR(1000),
                             user_id INT(50)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news 
                          (title, content, user_id) 
                          VALUES (?,?,?)''', (str(title), str(content), str(user_id)))
        cursor.close()
        self.connection.commit()

    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = {}".format(str(news_id), ))  # !!!!!!
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM news WHERE user_id = ?",
                           (str(user_id),))
        else:
            cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows

    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(news_id),))
        cursor.close()
        self.connection.commit()


class UserModel:
    def __init__(self, connection):
        self.connection = connection
        self.init_table()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128),
                             user_game INT(100) default 0,
                             user_factor INT(100) default 1
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, user_game, user_factor) 
                          VALUES (?,?,?,?)''', (user_name, password_hash, 0, 1))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def add_game(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE users SET user_game=user_game+user_factor WHERE id = {}".format(user_id))
        cursor.close()
        self.connection.commit()

    def add_factor(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE users SET user_factor=user_factor+1 WHERE id = {}".format(user_id))
        cursor.execute(
            "UPDATE users SET user_game=user_game-100 WHERE id = {}".format(user_id))
        cursor.close()
        print('1')
        self.connection.commit()

    def add_factor_2(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE users SET user_factor=user_factor+2 WHERE id = {}".format(user_id))
        cursor.execute(
            "UPDATE users SET user_game=user_game-200 WHERE id = {}".format(user_id))
        cursor.close()
        cursor.close()
        self.connection.commit()

    def add_factor_3(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE users SET user_factor=user_factor+3 WHERE id = {}".format(user_id))
        cursor.execute(
            "UPDATE users SET user_game=user_game-300 WHERE id = {}".format(user_id))
        cursor.close()
        cursor.close()
        self.connection.commit()

    def add_factor_4(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE users SET user_factor=user_factor+4 WHERE id = {}".format(user_id))
        cursor.execute(
            "UPDATE users SET user_game=user_game-400 WHERE id = {}".format(user_id))
        cursor.close()
        cursor.close()
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
            (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0], row[3], row[4]) if row else (False,)
