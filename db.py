import psycopg2
from psycopg2.extras import DictCursor
import configuration

current_configuration = configuration.get_current()
connection = psycopg2.connect(current_configuration.get_db_uri())


def bootstrap():
    cursor = connection.cursor(cursor_factory=DictCursor)
    query = "create table if not exists users(" \
            "id integer primary key, " \
            "username text, " \
            "sent boolean default false" \
            ")"
    cursor.execute(query)
    cursor.close()
    connection.commit()


def get_all_users(expression=None):
    cursor = connection.cursor(cursor_factory=DictCursor)
    query = "select * from users"
    if expression:
        query += f" where {expression}"
        cursor.execute(query, (expression, ))
    else:
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
    connection.commit()


def update_username(user_id, username):
    cursor = connection.cursor(cursor_factory=DictCursor)
    query = "update users set username = %s where id = %s"
    cursor.execute(query, (username, user_id))
    cursor.close()
    connection.commit()


def mark_as_sent(user_id):
    cursor = connection.cursor()
    query = "update users set sent = true where id = %s"
    cursor.execute(query, (user_id,))
    cursor.close()
    connection.commit()


def change_sent(value):
    cursor = connection.cursor()
    query = "update users set sent = %s"
    cursor.execute(query, (value,))
    cursor.close()
    connection.commit()


def delete_user(user_id):
    cursor = connection.cursor()
    query = "delete from users where id = %s"
    cursor.execute(query, (user_id,))
    cursor.close()
    connection.commit()


bootstrap()
