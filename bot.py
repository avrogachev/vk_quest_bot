from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher
from vk.keyboards import Keyboard, ButtonColor
from vk import types

import logging

from config import TOKEN, GROUP_ID#, PLUGINS_PATH #, loop
import keyboards

logging.basicConfig(level="DEBUG")

vk = VK(TOKEN)
gid = GROUP_ID
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)


@dp.message_handler(payload={"command": 'start'})
async def handle_start(message: types.Message, data: dict):
    await message.reply("Молодееец, начинаем работу с ботом! Получай клавиатуру", keyboard=kb_cpt.get_keyboard())


@dp.message_handler(text='hello')
async def handle_text_start(message: types.Message, data: dict):
    await message.reply("ты начал!")


@dp.message_handler(payload={"command": 'hello'})
async def handle_hello(message: types.Message, data: dict):
    await message.reply("payload hello")


@dp.message_handler(payload={"command": 'bye'})
async def handle_hello(message: types.Message, data: dict):
    await message.reply("payload bye")


@dp.message_handler(text="off")
async def off_keyboard(message: types.Message, data: dict):
    await message.answer("Ok.", keyboard=keyboard_start.get_keyboard())


@dp.message_handler()
async def handle_other_messages(message: types.Message, data: dict):
    await message.answer(message.text, keyboard=keyboard_start.get_keyboard() )#message.answer("another message", keyboard=keyboard.get_empty_keyboard())

async def run():
    await dp.run_polling()


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
