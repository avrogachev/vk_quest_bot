from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher, rules
from vk.bot_framework import BaseRule, BaseMiddleware
from vk import types

import logging

from config import TOKEN, GROUP_ID  # PLUGINS_PATH #, loop
from keyboards import *

logging.basicConfig(level="DEBUG")

vk = VK(TOKEN)
gid = GROUP_ID
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)


@dp.message_handler(rules.Command("start"))
async def handle(message: types.Message, data: dict):
    await message.reply("Hello!")


async def run():
    dp.run_polling()


if __name__ == "__main__":

    task_manager.add_task(run)
    task_manager.run()
