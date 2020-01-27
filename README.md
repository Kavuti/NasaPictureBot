# NasaPictureBot
This is the source code of the Telegram [@nasapicofthedaybot](https://t.me/nasapicofthedaybot). You can feel free of rehosting your version of this bot by modifying the source code. The bot is written in Python with the support of [Pyrogram](https://github.com/pyrogram/pyrogram).

NOTE: I'm currently working on the bot deploy so it's currently offline.

## Getting Started

### Prerequisites
To work on the source code of this bot, you will need to install Python 3.6+ and have a ready-to-use PostgreSQL database.

### Installation

In order to make the bot startable, you have to clone the repository and run the following command:
```
$ pip install -r requirements.txt
```

### Configuration
Once the process is finished, you can choose which type of configuration you want to adopt among:
* Environment Variables
* Configuration File

#### Environment Variables
If you choose this method, you will need to set 5 variables in your working system environment. They are:
* API_ID: It represents the Telegram API Id given to build Telegram applications. You can obtain one [here](https://my.telegram.org/apps)
* API_HASH: It represents the Telegram API Hash given to build Telegram applications. You can obtain one [here](https://my.telegram.org/apps)
* BOT_TOKEN: The bot token given by the [BotFather](https://t.me/BotFather).
* DATABASE_URL: The URL of your PostgreSQL database.
* NASA_API_KEY: Your NASA API Key. You can obtain one [here](https://api.nasa.gov)

#### Configuration File
If you choose this configuration method, you will need to set all the values in the file configuration/configuration.json
They are:
* api_id: It represents the Telegram API Id given to build Telegram applications. You can obtain one [here](https://my.telegram.org/apps)
* api_hash: It represents the Telegram API Hash given to build Telegram applications. You can obtain one [here](https://my.telegram.org/apps)
* bot_token: The bot token given by the [BotFather](https://t.me/BotFather).
* db_uri: The URL of your PostgreSQL database.
* nasa_api_key: Your NASA API Key. You can obtain one [here](https://api.nasa.gov)

## Execution
After the installation and configuration, you can start the bot easily by running
```
python3 main.py
```
