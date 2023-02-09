from pyrogram import Client, filters
from pyrogram.types import *

from config import *
from api import *
from user import *

app = Client("my_bot", 
                bot_token=BOT_TOKEN,
                api_id=API_ID,
                api_hash=API_HASH,
             )

async def search_movie_or_series(client:Client, message:Message, state:int):
    if len(message.text) > 60:
        await message.reply_text("Message is too long.")
        return
    
    resp = search_name(message.text, 1)
    
    if resp is None:
        await message.reply("Nothing found, Please try again.")
        return
    
    buttons = []
    
    for (text, data) in resp:
        buttons.append([
            InlineKeyboardButton(text, callback_data=data)]
        )
    
    buttons.append([InlineKeyboardButton("Next Page", callback_data='N1_{}'.format(message.text))])
    
    markup = InlineKeyboardMarkup(buttons)
    
    await message.reply_text(
        "Results for search: {} - page: {}".format(message.text, 1),
        reply_markup=markup
    )

async def send_item(client, chat_id, message_id, idd):
    item = select_item(idd)
    if item is None:
        await client.send_message(chat_id,
                                  "Wrong ID. Please try again.")
        return
    
    options = InlineKeyboardMarkup([
        [InlineKeyboardButton("Page in IMDB Website", 
                              url="https://www.imdb.com/title/{}/".format(idd))],
        [InlineKeyboardButton("Ratings", 
                              callback_data="R_{}".format(idd))],
        [InlineKeyboardButton("Screenshots", 
                              callback_data="S_{}".format(idd))],
    ])
    
    message, poster_name = generate_message(item)
    
    if message is None: 
        return
    if len(message) > 1023:
        try:
            await client.send_photo(chat_id, 
                                    poster_name, "Poster")
        except:
            pass
        await client.send_message(chat_id ,message, 
                                  reply_markup=options)
        return
    if poster_name is not None:
        try:
            await client.send_photo(chat_id, 
                                    poster_name, message, 
                                    reply_markup=options)
        except:
            pass
    else:
        await client.send_message(chat_id ,message, 
                                  reply_markup=options)
        
    await client.delete_messages(chat_id=chat_id,
                                 message_ids=message_id)
    
def get_page(search:str, page:int):
    resp = search_name(search, page)
    if resp is None:
        return None
    
    buttons = []
    
    for (text, data) in resp:
        buttons.append([InlineKeyboardButton(
            text, callback_data=data
            )])
        
    if page == 1:
        buttons.append([InlineKeyboardButton(
            "Next Page",
            callback_data='N{}_{}'.format(page, search)
            )])
        
    elif page == 100:
        buttons.append([InlineKeyboardButton(
            "Previous Page", 
            callback_data='P{}_{}'.format(page, search)
            )])
    else:
        buttons.append([
            InlineKeyboardButton(
                "Previous Page",
                callback_data='P{}_{}'.format(page, search)
                ),
            InlineKeyboardButton(
                "Next Page",
                callback_data='N{}_{}'.format(page, search)
                )
        ])
    return buttons

@app.on_message(filters.command('start'))
async def start(client:Client, message:Message):
    user_id = message.chat.id
    
    set_state(user_id, 0)
    
    await app.set_bot_commands(
        [BotCommand("start", 'start bot')]
    )
    await message.reply_text(HELLO_MESSAGE, reply_markup=reply_main_menu)

@app.on_message(filters.text & filters.private)
async def search(client:Client, message:Message):
    user_id = message.chat.id
    
    state = get_state(user_id)

    if state == 0:
        if message.text == "Search Movie or Series":
            await message.reply_text(SEARCH_MESSAGE,
                                     reply_markup=reply_back)
            set_state(user_id, 1)
            
        elif message.text == "Search by IMDB ID":
            await message.reply_text(IMDB_ID_MESSAGE, 
                                     reply_markup=reply_back)
            set_state(user_id, 2)
            
        else:
            await message.reply_text(WRONG_MESSAGE)
            
    elif message.text == "< back":
        set_state(user_id, 0)
        await message.reply_text(MAIN_MENU_MESSAGE, reply_markup=reply_main_menu)
        
    elif state == 1:
        await search_movie_or_series(client, message, state)
        
    elif state == 2:
        imdb_id = message.text
        message_id = message.id
        await send_item(client, user_id, message_id, imdb_id)
        
@app.on_callback_query()
async def answer(client:Client, callback_query:CallbackQuery):
    data = callback_query.data
    message_id = callback_query.message.id
    chat_id = callback_query.message.chat.id
    
    if data[0:1] == 'N' or data[0:1] == 'P':
        data = data.split('_')
        page = data[0]
        page = int(page[1:])
        search = data[1]
        
        if data[0][0:1] == 'N': 
            page += 1
            buttons = get_page(search, page)
            
        else: 
            page -= 1
            buttons = get_page(search, page)
            
        if buttons is None:
            await callback_query.answer(
                LAST_PAGE_MESSAGE,
                show_alert=True)
            return

        markup = InlineKeyboardMarkup(buttons)
        
        await callback_query.message.edit(
                                "Results for search: {} - Page: {}".format(search, page),
                                reply_markup=markup)
        
    elif data[0] == "S":
        data = data.split("_")
        idd = data[1]
        screenshots = get_screenshots(idd)
        
        if len(screenshots) == 0:
            await callback_query.answer(
                "Nothing found!",
                show_alert=True)
            return 
        
        for screenshot in screenshots:
            await callback_query.message.reply_photo(screenshot)
    
    elif data[0] == "R":
        data = data.split("_")
        idd = data[1]
        item = select_item(idd)
        
        if item["Ratings"] == "N/A":
            await callback_query.answer(
                "Nothing found!",
                show_alert=True)
            return
        
        else:
            m = ""
            for r in item["Ratings"]:
                m += r['Source'] + ": " + r["Value"] + "\n"
            if m == "":
                await callback_query.answer(
                    "Nothing found!",
                show_alert=True)
            else:
                await callback_query.message.reply_text(m)

    else:
        await send_item(client, chat_id, message_id, callback_query.data)
    try:
        await callback_query.answer(
            "Done!",
            show_alert=False)
    except:
        pass

app.run()