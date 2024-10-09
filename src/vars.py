import json
from loguru import logger

from config import *


commands = dict()
animals = dict()

active_quiz_sessions = {}
msg_for_forward = {}


try:
    with open(COMMANDS_PATH, encoding='utf-8') as file:
        commands = json.load(file)        
    with open(ANIMALS_PATH, encoding='utf-8') as file:
        animals = json.load(file)
except Exception as e:
    logger.error(e)
else:
    logger.success('Требуемые файлы успешно загружены')
