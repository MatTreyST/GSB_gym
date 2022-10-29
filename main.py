from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from telegram import Bot
from pseudo_db import *

TOKEN = "5501847639:AAGQM8XUrHcfbRBY442f5j9AJGYKlBfsgGE"
bot = Bot(TOKEN)
reservation_dict = {}
CHOOSE_FUNCTION = 1
SIGN_UP_OR_SHOW_EVENTS = 2
CHOOSE_DAY = 3
CHOOSE_TIME_FOR_INDIVIDUAL_SESSION = 4
CHOOSE_TIME_FOR_GROUP_SESSION = 5
ENTER_EMAIL = 6
ENTER_NAME = 7
FINAL = 8


def start(update: Update, context: CallbackContext) -> int:
    keys = [[InlineKeyboardButton("Let's go!", callback_data="start")]]
    reply_markup = InlineKeyboardMarkup(keys)
    update.message.reply_text(
        "Hello !\n\n"
        "Here U can find out about the upcoming events or sign up for the sport session in our new GSB gym\n\n"
        "Press 'Let's go' in order to get to the main menu", reply_markup=reply_markup)
    return CHOOSE_FUNCTION


def choose_an_option(update, context):
    query = update.callback_query
    query.answer()
    keys = [[InlineKeyboardButton("Sign up for the training", callback_data="sign_up_for_session")],
            [InlineKeyboardButton("Find out about the events", callback_data="show_events")]]
    reply_markup = InlineKeyboardMarkup(keys)
    query.edit_message_text(text="Choose the needed option", reply_markup=reply_markup)

    return SIGN_UP_OR_SHOW_EVENTS


def show_events(update, context):
    query = update.callback_query
    query.answer()
    keys = [[InlineKeyboardButton("Back", callback_data="start")]]
    reply_markup = InlineKeyboardMarkup(keys)
    query.edit_message_text("The only event which is going to happen is this bot getting 10/10 :)\n\n",
                            reply_markup=reply_markup)
    return CHOOSE_FUNCTION


def choose_group_or_individual(update, context):
    query = update.callback_query
    query.answer()
    keys = [[InlineKeyboardButton("Group", callback_data="group_session")],
            [InlineKeyboardButton("Individual", callback_data="self_session")]]
    reply_markup = InlineKeyboardMarkup(keys)
    query.edit_message_text("Choose what type of sport session you want to sign up for", reply_markup=reply_markup)
    return CHOOSE_DAY


def choose_day(update, context):
    query = update.callback_query
    query.answer()
    session_type = query.data
    keys = [[InlineKeyboardButton("Mon", callback_data="Monday")],
            [InlineKeyboardButton("Tue", callback_data="Tuesday")],
            [InlineKeyboardButton("Wed", callback_data="Wednesday")],
            [InlineKeyboardButton("Thu", callback_data="Thursday")],
            [InlineKeyboardButton("Fri", callback_data="Friday")],
            [InlineKeyboardButton("Sat", callback_data="Saturday")]]
    reply_markup = InlineKeyboardMarkup(keys)
    query.edit_message_text(text="Choose the day u want to visit us)", reply_markup=reply_markup)
    if session_type == "self_session":
        return CHOOSE_TIME_FOR_INDIVIDUAL_SESSION
    else:
        return CHOOSE_TIME_FOR_GROUP_SESSION


def choose_individual_time(update, context):
    query = update.callback_query
    query.answer()
    res_day = query.data
    user_id = query.from_user.id
    user_and_day_insert(user_id, res_day)
    if res_day == "Monday" or res_day == "Wednesday" or res_day == "Friday":
        keys = [[InlineKeyboardButton("10:00", callback_data="10")],
                [InlineKeyboardButton("14:00", callback_data="14")],
                [InlineKeyboardButton("19:00", callback_data="19")]]
    else:
        keys = [[InlineKeyboardButton("11:00", callback_data="11")],
                [InlineKeyboardButton("15:00", callback_data="15")],
                [InlineKeyboardButton("20:00", callback_data="20")]]
    reply_markup = InlineKeyboardMarkup(keys)
    query.edit_message_text("Choose the comfortable time 🕰\n\n"
                            "(except presented the gym is going to be working at full capacity)",
                            reply_markup=reply_markup)
    return FINAL


def choose_group_time(update, context):
    query = update.callback_query
    query.answer()
    res_day = query.data
    user_id = query.from_user.id
    user_and_day_insert(user_id, res_day)
    keys = [[InlineKeyboardButton("18:00", callback_data="18")]]
    reply_markup = InlineKeyboardMarkup(keys)
    query.edit_message_text("Choose the time for group training 🕰\n\n"
                            "(it is a 1-hour session)", reply_markup=reply_markup)
    return FINAL


def final(update, context):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    res_time = query.data
    day_and_time_list_insert(user_id, res_time)
    res_list = get_reservation_data(user_id)
    day = res_list[0]
    time = res_list[1]
    keys = [[InlineKeyboardButton("Continue", callback_data="start")]]
    reply_markup = InlineKeyboardMarkup(keys)
    query.edit_message_text(f"Congrats 🥳, u've signed up at {day} on {time}:00", reply_markup=reply_markup)
    return CHOOSE_FUNCTION


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSE_FUNCTION: [
                CallbackQueryHandler(choose_an_option, pattern="^start$")
            ],
            SIGN_UP_OR_SHOW_EVENTS: [
                CallbackQueryHandler(choose_group_or_individual, pattern="^sign_up_for_session$"),
                CallbackQueryHandler(show_events, pattern="^show_events$")
            ],
            CHOOSE_DAY: [
                CallbackQueryHandler(choose_day, pattern="^(group|self)_session$")
            ],
            CHOOSE_TIME_FOR_INDIVIDUAL_SESSION: [
                CallbackQueryHandler(choose_individual_time)
            ],
            CHOOSE_TIME_FOR_GROUP_SESSION: [
                CallbackQueryHandler(choose_group_time)
            ],
            FINAL: [
                CallbackQueryHandler(final)
            ]
        },
        fallbacks=[CommandHandler('start', start)],
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
