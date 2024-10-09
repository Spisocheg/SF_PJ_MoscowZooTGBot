from config import *
from src.exceptions_handler import *
from src.vars import *
from src import quiz

import re
from loguru import logger

import telebot

try:    
    bot = telebot.TeleBot(TOKEN, exception_handler=ExceptionHandler())
    telebot_logger = telebot.logger
    telebot_logger.setLevel(20)
except (Exception, ExceptionHandler) as e:
    logger.error(e)
else:
    logger.success('Бот успешно инициализирован')


@bot.message_handler(commands=['start', 'info'])
def start_help_command(message):
    bot.send_message(message.chat.id, commands["hello_message"], parse_mode='HTML')


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, commands["help_message"])


@bot.message_handler(commands=['guardianship'])
def quardianship_command(message):
    bot.send_message(message.chat.id, commands["guardianship"])


@bot.message_handler(commands=['contact'])
def contact_command(message):
    bot.send_message(message.chat.id, commands["contact"]+ADMIN_TAG)


@bot.message_handler(commands=['quiz'])
def quiz_command(message):
    quiz.quiz(bot, message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'restart')
def callback_restart(call):
    quiz.restart(bot, call)


@bot.callback_query_handler(func=lambda callback: callback.data in ['answ_0', 'answ_1'])
def callback_ques0(call):
    quiz.ques0(bot, call)


@bot.callback_query_handler(func=lambda callback: bool(re.search('^answ_[0,1][0,1]$', callback.data)))
def callback_ques1(call):
    quiz.ques1(bot, call)


@bot.callback_query_handler(func=lambda callback: bool(re.search('^answ_[0,1][0,1][0,1]$', callback.data)))
def callback_ques2(call):
    quiz.ques2(bot, call)


@bot.callback_query_handler(func=lambda callback: bool(re.search('^answ_[0,1][0,1][0,1][0,1]$', callback.data)))
def callback_ques3(call):
    quiz.ques3(bot, call)


@bot.callback_query_handler(func=lambda callback: callback.data in ['feedback'])
def callback_feedback(call):    
    bot.send_message(call.message.chat.id, commands["feedback"])
    bot.register_next_step_handler(call.message, feedback_register)


@bot.message_handler(commands=['feedback'])
def feedback_command(message):
    bot.send_message(message.chat.id, commands["feedback"])
    bot.register_next_step_handler(message, feedback_register)


def feedback_register(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.id)
    bot.send_message(message.chat.id, commands["fb_success"])


@bot.callback_query_handler(func=lambda callback: callback.data in ['contact'])
def callback_contact(call):
    bot.forward_message(ADMIN_ID, call.message.chat.id, msg_for_forward[call.message.chat.id].id)
    del msg_for_forward[call.message.chat.id]
    bot.send_message(call.message.chat.id, commands["contact_success"]+ADMIN_TAG)


if __name__ == "__main__":
    logger.info('Запуск бота...')
    try:
        bot.infinity_polling()
    except ExceptionHandler as e:
        logger.critical(e)
    else:
        logger.info('Бот прекратил работу')
