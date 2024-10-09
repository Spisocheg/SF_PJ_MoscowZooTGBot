from telebot import types

from .vars import *


def quiz(bot, message):
    try:
        tmp = active_quiz_sessions[message.chat.id]
    except:
        kb = types.InlineKeyboardMarkup()
        kb.row_width = 1
        kb.add(types.InlineKeyboardButton(commands["answers"][0][0], callback_data="answ_0"),
                types.InlineKeyboardButton(commands["answers"][0][1], callback_data="answ_1"))
        
        msg1 = bot.send_message(message.chat.id, commands["welcome_test_message"])
        msg2 = bot.send_message(message.chat.id, f'{commands["questions"][0]}\n\n{commands["try_again"]}', reply_markup=kb, parse_mode='HTML')
        
        active_quiz_sessions[message.chat.id] = [msg1, msg2]
    else:
        kb = types.InlineKeyboardMarkup()
        kb.row_width = 1
        kb.add(types.InlineKeyboardButton('Да, подтверждаю', callback_data='restart'))

        bot.send_message(message.chat.id, commands["warning"], reply_markup=kb)


def restart(bot, call):
    bot.delete_messages(call.message.chat.id, [msg.id for msg in active_quiz_sessions[call.message.chat.id]])
    bot.delete_message(call.message.chat.id, call.message.id)
    del active_quiz_sessions[call.message.chat.id]


def ques0(bot, call):
    kb = types.InlineKeyboardMarkup()
    kb.row_width = 1
    kb.add(types.InlineKeyboardButton(commands["answers"][1][0], callback_data=f"{call.data}0"),
            types.InlineKeyboardButton(commands["answers"][1][1], callback_data=f"{call.data}1"))

    msg = bot.send_message(call.message.chat.id, f'{commands["questions"][1]}\n\n{commands["try_again"]}', reply_markup=kb, parse_mode='HTML')
    active_quiz_sessions[call.message.chat.id].append(msg)


def ques1(bot, call):
    kb = types.InlineKeyboardMarkup()
    kb.row_width = 1
    kb.add(types.InlineKeyboardButton(commands["answers"][2][0], callback_data=f"{call.data}0"),
            types.InlineKeyboardButton(commands["answers"][2][1], callback_data=f"{call.data}1"))
    
    msg = bot.send_message(call.message.chat.id, f'{commands["questions"][2]}\n\n{commands["try_again"]}', reply_markup=kb, parse_mode='HTML')
    active_quiz_sessions[call.message.chat.id].append(msg)


def ques2(bot, call):
    kb = types.InlineKeyboardMarkup()
    kb.row_width = 1
    kb.add(types.InlineKeyboardButton(commands["answers"][3][0], callback_data=f"{call.data}0"),
            types.InlineKeyboardButton(commands["answers"][3][1], callback_data=f"{call.data}1"))
    
    msg = bot.send_message(call.message.chat.id, f'{commands["questions"][3]}\n\n{commands["try_again"]}', reply_markup=kb, parse_mode='HTML')
    active_quiz_sessions[call.message.chat.id].append(msg)


def get_result(calldata):
    num = calldata.replace('answ_', '')
    selector = [
        animals["translator"][f"{num[0]}000"],
        animals["translator"][f"{num[1]}00"],
        animals["translator"][f"{num[2]}0"],
        animals["translator"][f"{num[3]}"],
    ]
    return animals[selector[0]][selector[1]][selector[2]][selector[3]]


def ques3(bot, call):
    del active_quiz_sessions[call.message.chat.id]
    
    result = get_result(call.data)
    text = f'{commands["result_message"]["header"]}\n\n{result["name"]}\n{result["description"]}\
    \n\n\n{commands["result_message"]["footer"]["ad"]}\n\n{commands["result_message"]["footer"]["contact"]}\
    \n\n\n{commands["result_message"]["footer"]["one_more_time"]}'
    
    kb = types.InlineKeyboardMarkup()
    kb.row_width = 1
    kb.add(types.InlineKeyboardButton("Оставить отзыв", callback_data="feedback"),
           types.InlineKeyboardButton("Связаться с сотрудником", callback_data="contact"))

    msg = bot.send_photo(call.message.chat.id, photo=result["path"], caption=text, reply_markup=kb)
    msg_for_forward[call.message.chat.id] = msg
