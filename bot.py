from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher
from vk.keyboards import Keyboard, ButtonColor
from vk import types

import logging

from config import TOKEN, GROUP_ID#, PLUGINS_PATH #, loop

logging.basicConfig(level="DEBUG")

vk = VK(TOKEN)
gid = GROUP_ID
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)

keyboard1 = Keyboard(one_time=False)
keyboard1.add_text_button('Hi', payload={"command": 'hello'})
keyboard1.add_text_button("Bye:(", payload={"command": 'bye'}, color=ButtonColor.SECONDARY)

keyboard_start = Keyboard(one_time=True)
keyboard_start.add_text_button('Начинаем квест!', payload={"command": 'start'})


@dp.message_handler(payload={"command": 'start'})
async def handle_start(message: types.Message, data: dict):
    await message.reply("МОлодееец, начинаем работу с ботом! Получай клавиатуру", keyboard=keyboard1.get_keyboard())


@dp.message_handler(text='hello')
async def handle_text_start(message: types.Message, data: dict):
    await message.reply("ты начал!")


@dp.message_handler(payload={"command": 'hello'})
async def handle_hello(message: types.Message, data: dict):
    await message.reply("payload hello")


#@dp.message_handler(payload=["bye", "test", "start", "aoff"])
#async def handle(message: types.Message, data: dict):
#    await message.reply("Bye!")


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
