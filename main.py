import flask
import os
import configuration
import requests
import schedule
import time
import db
from pyrogram import Client, Filters
from pyrogram.errors import BadRequest
from flask import *

conf = configuration.get_current()
bot = Client(":memory:", bot_token=conf.get_bot_token(), api_id=conf.get_api_id(), api_hash=conf.get_api_hash())
nasa_url = f'https://api.nasa.gov/planetary/apod?api_key={conf.get_nasa_api_key()}'
request_session = requests.Session()

db_initialized = False
logger = conf.get_logger()

flask_app = Flask(__name__)


def get_photo():
    return request_session.get(nasa_url)


def pre_operations(message):
    global db_initialized
    if not db_initialized:
        db.bootstrap()
        db_initialized = True
    user = db.get_user(message.from_user.id)
    if not user:
        logger.info("Inserting user")
        db.insert_user(message.from_user.id, message.from_user.username)
    else:
        logger.info("Updating user")
        db.update_username(message.from_user.id, message.from_user.username)


@bot.on_message(Filters.command("start"))
def start_command(client, message):
    pre_operations(message)
    message.reply("Hi, this is a bot that sends you the NASA's picture of the day.")


@bot.on_message(Filters.command("get"))
def send_picture(client, message):
    pre_operations(message)
    user = db.get_user(message.from_user.id)
    logger.info(f'The user {user["username"]} ({user["id"]}) requested his image now.')
    json_resp = get_photo().json()
    bot.send_photo(message.from_user.id, json_resp['hdurl'])
    message_string = f"Hi! This is the image of today. Enjoy it!\n" \
                     f"**{json_resp['title']}**\n\n" \
                     f"{json_resp['explanation']}"
    if 'copyright' in json_resp:
        message_string += f"\n\n__© {json_resp['copyright']}__"

    bot.send_message(user['id'], message_string)
    db.mark_as_sent(user['id'])


def send_picture_to_all():
    logger.info("Sending today's picture to all users")
    json_resp = get_photo().json()
    users = db.get_all_users("sent = false")
    if users:
        for user in users:
            try:
                bot.send_photo(user['id'], json_resp['hdurl'])
                message_string = f"Hi! This is the image of today. Enjoy it!\n" \
                                 f"**{json_resp['title']}**\n\n" \
                                 f"{json_resp['explanation']}"
                if 'copyright' in json_resp:
                    message_string += f"\n\n__© {json_resp['copyright']}__"

                bot.send_message(user['id'], message_string)

            except BadRequest:
                logger.error(f'Bad request sending picture to user @{user["username"]} '
                             f'({user["id"]}). Deleting the user.')
                db.delete_user(user['id'])
        db.change_sent(True)


def reset_users_sent():
    logger.info("Resetting sent for all users")
    db.change_sent(False)


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=os.environ.get('PORT') or 5000)
    schedule.every().day.at("09:00").do(send_picture_to_all)
    schedule.every().day.at("00:00").do(reset_users_sent)

    with bot:
        while True:
            schedule.run_pending()
            time.sleep(1)
