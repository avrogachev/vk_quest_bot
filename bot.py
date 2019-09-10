mport logging
from vk import types
from vk import BackgroundTask
from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher, Storage
# from vk.bot_framework import Storage


from config import TOKEN, GROUP_ID  # PLUGINS_PATH #, loop
from keyboards import *

logging.basicConfig(level="DEBUG")

vk = VK(TOKEN)
gid = GROUP_ID
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)

storage = Storage()
dp.storage = storage

really_needed_counter = 0

dp.storage.place("really_needed_counter", really_needed_counter)

@dp.message_handler(payload={"command": 'start'})
async def handle_start(message: types.Message, data: dict):
    async with BackgroundTask(very_slow_operation, 5) as task:
        await task()
    await message.reply("Космический рейс в лице бота Афанасия приветствует тебя!\n"
                        "Капитан должен зарегистрировать команду. "
                        "Как только он закончит, присоединяйтесь к нему и бегом в игру!",
                        keyboard=kb_choose.get_keyboard())
@dp.message_handler(payload={"command": 'kb_choose_captain'})
async def handle_choose_captain(message: types.Message, data: dict):
    await message.reply("Как называется твоя команда? Если ты не капитан, жми кнопку \"Назад\" ",
                        keyboard=kb_back_to_start.get_keyboard())
@dp.message_handler(payload={"command": 'kb_choose_participant'})
async def handle_choose_participant(message: types.Message, data: dict):
    await message.reply("Дождись, пока капитан зарегистрируется и скажи мне название твоей команды. "
                        "Если ты капитан, жми кнопку \"Назад\"", keyboard=kb_back_to_start.get_keyboard())
@dp.message_handler(payload={"command": 'kb_back_to_start'})
async def handle_back_to_start(message: types.Message, data: dict):
    await message.reply("В этот раз будь внимательнее:)", keyboard=kb_choose.get_keyboard())
@dp.message_handler(payload={"command": 'tasks'})
async def handle_tasks(message: types.Message, data: dict):
    c = dp.storage.get("really_needed_counter", 0)
    await message.reply("Тут будет список заданий.")
    dp.storage.update("really_needed_counter", c + 1)
    await message.answer(f"Hello! {c}")
@dp.message_handler(payload={"command": 'help'})
async def handle_help(message: types.Message, data: dict):
    await message.reply("Сейчас с вами свяжется агент из штаба, бот:(")
@dp.message_handler(payload={"command": 'marks'})
async def handle_marks(message: types.Message, data: dict):
    await message.reply("Тут будут баллы команды.")
@dp.message_handler(commands=["buy"], have_args=[lambda arg: arg.isdigit(), lambda arg: arg > 10])
async def handler(message: types.Message, data: dict):
    """
    Validate args. You may add to list lambda`s, or sync func`s with 1 arg (arg) and returned bool-like value.
    """
    await message.answer("Ok.")

@dp.message_handler()  # обработка названий команды. TODO: машина состояний для определения момента ввода команды
async def handle_other_messages(message: types.Message, data: dict):
    await message.answer(message.text, keyboard=kb_main.get_keyboard())

def very_slow_operation(a: int):
    import time

    time.sleep(10)
    print(a + 10)

async def run():
    await dp.run_polling()


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
