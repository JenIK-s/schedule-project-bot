from datetime import datetime, date
import os
from dotenv import load_dotenv


from telegram.ext import CommandHandler, CallbackQueryHandler, Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from functions import forming_string, add_user_to_database, get_group

load_dotenv()
updater = Updater(token=os.getenv('TOKEN'))
day_of_the_week: int = date.today().weekday()

week_number = datetime.today().isocalendar()[1]


def handle_button_press(update, context):
    global day_of_the_week

    query = update.callback_query
    user_id = update.effective_chat.id
    button_data = query.data
    buttons_schedule = [
        [
            InlineKeyboardButton(
                'Расписание на сегодня', callback_data='schedule_today'
            )
        ],
        [
            InlineKeyboardButton(
                'Расписание на завтра', callback_data='schedule_tomorrow'
            )
        ],
        [
            InlineKeyboardButton(
                'Расписание на неделю', callback_data='schedule_weekly'
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(buttons_schedule)
    if day_of_the_week % 2 == 0:
        week = 'Числитель'
    else:
        week = 'Знаменатель'
    match button_data:
        case 'one' | 'two':
            try:
                add_user_to_database(user_id, button_data)
                context.bot.send_message(chat_id=user_id,
                                         text='Выберите расписание',
                                         reply_markup=reply_markup
                                         )
            except:
                context.bot.send_message(
                    chat_id=user_id,
                    text='Вы уже выбрали подгруппу, выберите расписание',
                    reply_markup=reply_markup
                )
        case 'schedule_today':
            try:
                group = get_group(user_id)
                result_string = forming_string(week, group, day_of_the_week)
                context.bot.send_message(chat_id=user_id,
                                         text=result_string,
                                         reply_markup=reply_markup,
                                         )
            except:
                context.bot.send_message(chat_id=user_id,
                                         text='Ошибка отправки...',
                                         reply_markup=reply_markup,
                                         )
        case 'schedule_tomorrow':
            try:
                group = get_group(user_id)
                if day_of_the_week == 6:
                    day_of_the_week = 0
                    week = 'Знаменатель'
                else:
                    day_of_the_week += 1
                result_string = forming_string(week, group, day_of_the_week)
                context.bot.send_message(chat_id=user_id,
                                         text=result_string,
                                         reply_markup=reply_markup,
                                         )
            except:
                context.bot.send_message(chat_id=user_id,
                                         text='Ошибка отправки...',
                                         reply_markup=reply_markup,
                                         )
        case 'schedule_weekly':
            try:
                group = get_group(user_id)
                for day in range(7):
                    result_string = forming_string(week, group, day)
                    context.bot.send_message(chat_id=user_id,
                                             text=result_string,
                                             reply_markup=reply_markup,
                                             )
            except:
                context.bot.send_message(chat_id=user_id,
                                         text='Ошибка отправки...',
                                         reply_markup=reply_markup,
                                         )


def start(update, context):
    chat = update.effective_chat
    buttons_group = [
        InlineKeyboardButton('✅ 1 Подгруппа', callback_data='one'),
        InlineKeyboardButton('✅ 2 Подгруппа', callback_data='two'),
    ]
    reply_markup = InlineKeyboardMarkup([buttons_group])
    context.bot.send_message(
        chat_id=chat.id,
        text='Выберите подгруппу',
        reply_markup=reply_markup
    )


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(handle_button_press))

updater.start_polling()
updater.idle()
