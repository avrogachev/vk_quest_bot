from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher
from vk import types

import logging

from config import TOKEN, GROUP_ID#, PLUGINS_PATH #, loop
from keyboards import *

logging.basicConfig(level="DEBUG")

vk = VK(TOKEN)
gid = GROUP_ID
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)


@dp.message_handler(payload={"command": 'start'})
async def handle_start(message: types.Message, data: dict):
    await message.reply("Космический рейс в лице бота Афанасия приветсвует тебя!\n"
                        "Капитан должен зарегистрировать команду. "
                        "Как только он закончит, присоединяйтесь к нему и бегом в игру!", keyboard=kb_choose.get_keyboard())


@dp.message_handler(payload={"command": 'kb_choose_captain'})
async def handle_choose_captain(message: types.Message, data: dict):
    await message.reply("Как называется твоя команда? Если ты не капитан, жми кнопку \"Назад\" ", keyboard=kb_back_to_start.get_keyboard())


@dp.message_handler(payload={"command": 'kb_choose_participant'})
async def handle_choose_participant(message: types.Message, data: dict):
    await message.reply("Дождись, пока капитан зарегистрируется и скажи мне название твоей команды. "
                        "Если ты капитан, жми кнопку \"Назад\"", keyboard=kb_back_to_start.get_keyboard())


@dp.message_handler(payload={"command": 'kb_back_to_start'})
async def handle_back_to_start(message: types.Message, data: dict):
    await message.reply("В этот раз будь внимательнее:)", keyboard=kb_choose.get_keyboard())


@dp.message_handler(payload={"command": 'tasks'})
async def handle_tasks(message: types.Message, data: dict):
    await message.reply("Тут будет список заданий.")


@dp.message_handler(payload={"command": 'help'})
async def handle_help(message: types.Message, data: dict):
    await message.reply("Сейчас с вами свяжется агент из штаба, боту не помочь:(")


@dp.message_handler(payload={"command": 'marks'})
async def handle_marks(message: types.Message, data: dict):
    await message.reply("Тут будет список заданий.")


@dp.message_handler()  # обработка названий команды. TODO: машина состояний для определения момента ввода команды
async def handle_other_messages(message: types.Message, data: dict):
    await message.answer(message.text, keyboard=kb_main.get_keyboard())

async def run():
    await dp.run_polling()


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
