from pyrogram.types import *

HELLO_MESSAGE = """Hi,
Please choose from the menu."""

SEARCH_MESSAGE  = "Enter Movie or series name"

MAIN_MENU_MESSAGE = """Main Menu"""

IMDB_ID_MESSAGE = "Enter IMDB ID: (example: tt1234567)"

LAST_PAGE_MESSAGE = """This is Last Page."""

WRONG_MESSAGE = "Wrong Command."

BOT_TOKEN = ""

API_ID = 123

API_HASH = ""

reply_main_menu = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Search Movie or Series")],
        [KeyboardButton("Search by IMDB ID")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

reply_back = ReplyKeyboardMarkup(
    [
        [KeyboardButton("< back")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
