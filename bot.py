from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher
from vk import types

import logging

from config import TOKEN, GROUP_ID#, PLUGINS_PATH #, loop

logging.basicConfig(level="INFO")

vk = VK(TOKEN)
gid = GROUP_ID
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)


@dp.message_handler(commands=["help", "test", "start", "aoff"])
async def handle(message: types.Message, data: dict):
    await message.reply("Test!")


@dp.message_handler(text="hello")
async def handle_event(message: types.Message, data: dict):
    await message.reply("Hello!")


async def run():
    await dp.run_polling()


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
