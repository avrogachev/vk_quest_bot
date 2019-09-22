import logging
from vk import types
from vk import BackgroundTask
from vk.bot_framework import BaseRule, BaseMiddleware, rules
from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher
from vk.bot_framework import Storage
from vk.bot_framework.addons import cooldown
import emoji  # https://www.webfx.com/tools/emoji-cheat-sheet/


from config import TOKEN, GROUP_ID  # PLUGINS_PATH #, loop
from keyboards import *

logging.basicConfig(level="DEBUG")

vk = VK(TOKEN)
gid = GROUP_ID
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)

TEXT = {1: 'first задание',
        2: 'second задание',
        3: 'third задание'}
USERS = {}  # schema - id: lead, user, agent dict of dicts????????? it is the solution!!!
TEAMS = {}  # schema - id: team_id = captain_id
LEADS = {}
progress = {}  # schema - team_name: something to pass progress on stages
AGENTS = {}  # schema - id: stage
ADMINS = {182840420: 'admin'}  # schema - id: status


class RegistrationMiddleware(BaseMiddleware):
    """
    Register users in bot.
    """
    async def pre_process_event(self, event, data: dict):
        if event["type"] == "message_new":
            from_id = event["object"]["from_id"]
            if from_id not in USERS:
                USERS[from_id] = "user"
        return data

    async def post_process_event(self):
        pass


class IsAdmin(BaseRule):
    """
    Check admin rights of user.
    """

    def __init__(self, is_admin: bool):
        self.is_admin: bool = is_admin

    async def check(self, message: types.Message, data: dict):
        status = ADMINS[message.from_id]
        if not self.is_admin and status != "admin":
            return True
        elif not self.is_admin and status == "admin":
            return False
        elif self.is_admin and status == "admin":
            return True
        elif self.is_admin and status != "admin":
            return False


class IsLeadChoose(BaseRule):
    """
    Проверка, является ли человек капитаном команды
    """
    async def check(self, message: types.Message, data: dict):
        status = USERS[message.from_id]
        if status == "lead_choose":
            return True
        else:
            return False


class IsUserChoose(BaseRule):
    """
    Проверка, является ли человек капитаном команды
    """
    async def check(self, message: types.Message, data: dict):
        status = USERS[message.from_id]
        if status == "user_choose":
            return True
        else:
            return False


storage = Storage()
dp.storage = storage
cooldown.set_cooldown_message(
    "Подождите секундочку {cooldown} ..."
)  # or use standart message

really_needed_counter = 0

dp.storage.place("really_needed_counter", really_needed_counter)


@dp.message_handler(text="text")
@cooldown.cooldown_handler(
    storage, cooldown_time=10, for_specify_user=True
)  # have a simply design
async def test(msg: types.Message, data):
    await msg.answer("Hello!")


@dp.message_handler(payload={"command": 'start'})
async def handle_start(message: types.Message, data: dict):
    async with BackgroundTask(very_slow_operation, 5) as task:
        await task()
    await message.reply("Космический рейс в лице бота Афанасия приветствует тебя!\n"
                        "Капитан должен зарегистрировать команду. "
                        "Как только он закончит, присоединяйтесь к нему и бегом в игру!",
                        keyboard=kb_choose.get_keyboard())


@dp.message_handler(rules.Command("init"))
async def handle_start_another(message: types.Message, data: dict):
    await message.reply("Космический рейс в лице бота Афанасия приветствует тебя!\n"
                        "Капитан должен зарегистрировать команду. "
                        "Как только он закончит, присоединяйтесь к нему и бегом в игру!",
                        keyboard=kb_choose.get_keyboard())


@dp.message_handler(payload={"command": 'kb_choose_captain'})
async def handle_choose_captain(message: types.Message, data: dict):
    USERS[message.from_id] = "lead_choose"
    await message.reply("Как называется твоя команда? Если ты не капитан, жми кнопку \"Назад\" ",
                        keyboard=kb_back_to_start.get_keyboard())


@dp.message_handler(payload={"command": 'kb_choose_participant'})
async def handle_choose_participant(message: types.Message, data: dict):
    USERS[message.from_id] = "user_choose"
    await message.reply("Дождись, пока капитан зарегистрируется и скажи мне название твоей команды. "
                        "Если ты капитан, жми кнопку \"Назад\"", keyboard=kb_back_to_start.get_keyboard())


@dp.message_handler(payload={"command": 'kb_back_to_start'})
async def handle_back_to_start(message: types.Message, data: dict):
    USERS[message.from_id] = "user"
    await message.reply("В этот раз будь внимательнее:)", keyboard=kb_choose.get_keyboard())


@dp.message_handler(payload={"command": 'tasks'})
async def handle_tasks(message: types.Message, data: dict):
    # c = dp.storage.get("really_needed_counter", 0)
    await message.reply(emoji.emojize('Тут мне нужно собрать табличку вида:'
                                      '\n Чтобы решить загадку и увидеть её целиком, пришли мне её номер '
                                      '(просто числом, например, 2)'
                                      '\n1. :key:' '8391 :white_check_mark: '
                                      '\n 2. :x: \n3. :x:'))
    # dp.storage.update("really_needed_counter", c + 1)
    # await message.answer(f"Hello! {c}")


@dp.message_handler(payload={"command": 'help'})
async def handle_help(message: types.Message, data: dict):
    await message.reply("Сейчас с вами свяжется агент из штаба, бот:(")


@dp.message_handler(payload={"command": 'marks'})
async def handle_marks(message: types.Message, data: dict):
    await message.reply("Тут будут баллы команды.")


@dp.message_handler(rules.Command("admin"), IsAdmin(True))
async def admin_panel(message: types.Message, data: dict):
    await message.reply("Is admin panel! \U0001f600")


@dp.message_handler(rules.Command("teams"), IsAdmin(True))
async def admin_list_of_teams(message: types.Message, data: dict):
    await message.reply("Is admin panel! \U0001f600" + TEAMS.items())


@dp.message_handler(rules.Command("get"), IsAdmin(False))
async def get_admin_rights(message: types.Message, data: dict):
    USERS[message.from_id] = "admin"
    await message.reply("Successfully! \U0001f600")


@dp.message_handler(rules.Command("buy"), have_args=[lambda arg: arg.isdigit(), lambda arg: arg > 10])
async def handle_arg_command(message: types.Message, data: dict):
    """
    Validate args. You may add to list lambda`s, or sync func`s with 1 arg (arg) and returned bool-like value.
    """
    await message.answer("Ok.")


@dp.message_handler(text="1")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_1_riddle(message: types.Message, data: dict):
    await message.answer(TEXT[1], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="2")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_2_riddle(message: types.Message, data: dict):
    await message.answer(TEXT[1], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="3")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_3_riddle(message: types.Message, data: dict):
    await message.answer(TEXT[3], keyboard=kb_main.get_keyboard())


@dp.message_handler(IsLeadChoose())  # обработка названий команды. TODO: машина состояний
async def handle_lead_chooses_team_name(message: types.Message, data: dict):
    USERS[message.from_id] = "lead"
    TEAMS[message.from_id] = message.text
    await message.answer("Ура, команда %s зарегистрирована!" % TEAMS[message.from_id], keyboard=kb_main.get_keyboard())


@dp.message_handler(IsUserChoose())  # обработка названий команды
async def handle_user_choose_team(message: types.Message, data: dict):
    for ids, names in TEAMS.items():
        if names == message.text:
            USERS[message.from_id] = "user"
            TEAMS[message.from_id] = id
            # поменяли статус на юзер с юзер_чуз. Также надо проассоциировать команду
            await message.answer("Отлично, теперь вы член команды %s. Бегом в игру!" % message.text, keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Не вижу такой команды... Посмотри у капитана, как он её записал и попробуй ещё раз.")


def very_slow_operation(a: int):
    import time

    time.sleep(10)
    print(a + 10)


async def run():
    await dp.run_polling()


if __name__ == "__main__":
    dp.setup_middleware(RegistrationMiddleware())  # setup middleware

    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
