import psycopg2
from psycopg2.extras import DictCursor
import configuration

current_configuration = configuration.get_current()
connection = psycopg2.connect(current_configuration.get_db_uri())


def bootstrap():
    cursor = connection.cursor(cursor_factory=DictCursor)
    query = "create table if not exists users(id integer primary key, username text)"
    cursor.execute(query)
    cursor.close()


def get_all_users():
    cursor = connection.cursor(cursor_factory=DictCursor)
    query = "select * from users"
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    return users


def get_user(user_id):
    cursor = connection.cursor(cursor_factory=DictCursor)
    query = "select * from users where id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    cursor.close()
    if result:
        return result[0]
    else:
        return None


def insert_user(user_id, username):
    cursor = connection.cursor(cursor_factory=DictCursor)
    query = "insert into users values(%s, %s)"
    cursor.execute(query, (user_id, username))
    cursor.close()


def update_user(user_id, username):
    cursor = connection.cursor(cursor_factory=DictCursor)
    query = "update users set username = %s where id = %s"
    cursor.execute(query, (username, user_id))
    cursor.close()


bootstrap()
