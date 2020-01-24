import configuration
import requests
import schedule
import time
import db
from pyrogram import Client, Filters

conf = configuration.get_current()
bot = Client(":memory:", bot_token=conf.get_bot_token(), api_id=conf.get_api_id(), api_hash=conf.get_api_hash())
nasa_url = f'https://api.nasa.gov/planetary/apod?api_key={conf.get_nasa_api_key()}'
request_session = requests.Session()

db_initialized = False


def pre_operations(message):
    global db_initialized
    if not db_initialized:
        db.bootstrap()
        db_initialized = True
    user = db.get_user(message.from_user.id)
    if not user:
        db.insert_user(message.from_user.id, message.from_user.username)
    else:
        db.update_user(message.from_user.id, message.from_user.username)


@bot.on_message(Filters.command("start"))
def start_command(client, message):
    pre_operations(message)
    message.reply("Hi, this is a bot that sends you the NASA's picture of the day.")


@bot.on_message(Filters.command("get"))
def send_picture(client, message):
    pre_operations(message)
    json_resp = request_session.get(nasa_url).json()
    bot.send_photo(message.from_user.id, json_resp['hdurl'])
    bot.send_message(message.from_user.id, f"Hi! This is the image of today. Enjoy it!\n"
                                           f"**{json_resp['title']}**\n\n"
                                           f"{json_resp['explanation']}\n\n"
                                           f"__© {json_resp['copyright']}__")


def send_picture_to_all():
    json_resp = request_session.get(nasa_url).json()
    users = db.get_all_users()
    if users:
        for user in users:
            bot.send_photo(user['id'], json_resp['hdurl'])
            bot.send_message(user['id'], f"Hi! This is the image of today. Enjoy it!\n"
                                           f"**{json_resp['title']}**\n\n"
                                           f"{json_resp['explanation']}\n\n"
                                           f"__© {json_resp['copyright']}__")


schedule.every().day.at("09:00").do(send_picture_to_all)

with bot:
    while True:
        schedule.run_pending()
        time.sleep(1)
