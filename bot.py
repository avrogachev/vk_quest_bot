import logging
from vk import types
from vk.bot_framework import BaseRule, BaseMiddleware, rules
from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher
from vk.bot_framework import Storage
import emoji  # https://www.webfx.com/tools/emoji-cheat-sheet/


from config import TOKEN, GROUP_ID  # PLUGINS_PATH #, loop
from keyboards import *

logging.basicConfig(level="INFO")

vk = VK(TOKEN)
gid = GROUP_ID
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)

TEXT = {1: 'first задание',
        2: 'second задание',
        3: 'third задание'}
USERS = {}  # schema - id: lead, user, agent dict of dicts????????? it is the solution!!!
TEAMS = {}  # schema - team_id: {всё по тиме и задачкам}
LEADS = {}  # schema - id: lead_id
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
                USERS[from_id] = "new"
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


class IsNew(BaseRule):
    """
    Check admin rights of user.
    """

    def __init__(self, is_admin: bool):
        self.is_admin: bool = is_admin

    async def check(self, message: types.Message, data: dict):
        status = USERS[message.from_id]
        if not self.is_admin and status != "new":
            return True
        elif not self.is_admin and status == "new":
            return False
        elif self.is_admin and status == "new":
            return True
        elif self.is_admin and status != "new":
            return False


class IsLeadChoose(BaseRule):
    """
    Проверка статуса капитана
    """

    def __init__(self, is_admin: bool):
        self.is_admin: bool = is_admin

    async def check(self, message: types.Message, data: dict):
        status = USERS[message.from_id]
        if not self.is_admin and status != "lead_choose":
            return True
        elif not self.is_admin and status == "lead_choose":
            return False
        elif self.is_admin and status == "lead_choose":
            return True
        elif self.is_admin and status != "lead_choose":
            return False


class IsLead(BaseRule):
    """
    Проверка статуса капитана
    """

    def __init__(self, is_admin: bool):
        self.is_admin: bool = is_admin

    async def check(self, message: types.Message, data: dict):
        status = USERS[message.from_id]
        if not self.is_admin and status != "lead":
            return True
        elif not self.is_admin and status == "lead":
            return False
        elif self.is_admin and status == "lead":
            return True
        elif self.is_admin and status != "lead":
            return False


class IsUser(BaseRule):
    """
    Проверка статуса капитана
    """

    def __init__(self, is_admin: bool):
        self.is_admin: bool = is_admin

    async def check(self, message: types.Message, data: dict):
        status = USERS[message.from_id]
        if not self.is_admin and status != "user":
            return True
        elif not self.is_admin and status == "user":
            return False
        elif self.is_admin and status == "user":
            return True
        elif self.is_admin and status != "user":
            return False


class IsUserChoose(BaseRule):
    """
    Проверка статуса члена команды
    """

    def __init__(self, is_admin: bool):
        self.is_admin: bool = is_admin

    async def check(self, message: types.Message, data: dict):
        status = USERS[message.from_id]
        if not self.is_admin and status != "user_choose":
            return True
        elif not self.is_admin and status == "user_choose":
            return False
        elif self.is_admin and status == "user_choose":
            return True
        elif self.is_admin and status != "user_choose":
            return False


storage = Storage()
dp.storage = storage


@dp.message_handler(payload={"command": 'start'})
async def handle_start(message: types.Message, data: dict):
    await message.reply("Космический рейс в лице бота Афанасия приветствует тебя!\n"
                        "Капитан должен зарегистрировать команду. "
                        "Как только он закончит, присоединяйтесь к нему и бегом в игру!",
                        keyboard=kb_choose.get_keyboard())


@dp.message_handler(rules.Command("init"))
async def handle_start_another(message: types.Message, data: dict):
    await message.reply("Здравствуй! Космический рейс в лице бота Афанасия приветствует тебя!\n"
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
    await message.reply("Дождись, пока капитан зарегистрируется и напиши мне код команды - он появится у капитана. "
                        "Если ты капитан, жми кнопку \"Назад\"", keyboard=kb_back_to_start.get_keyboard())


@dp.message_handler(payload={"command": 'kb_back_to_start'})
async def handle_back_to_start(message: types.Message, data: dict):
    USERS[message.from_id] = "new"
    await message.reply("В этот раз будь внимательнее:)", keyboard=kb_choose.get_keyboard())


@dp.message_handler(payload={"command": 'tasks'})
async def handle_tasks(message: types.Message, data: dict):
    await message.reply('Тут мне нужно собрать табличку вида:'
                                      '\n Чтобы решить загадку и увидеть её целиком, пришли мне её номер '
                                      '(просто числом, например, 2)'
                                      '\n1. :key:' '8391 :white_check_mark: '
                                      '\n 2. :x: \n3. :x:')


@dp.message_handler(payload={"command": 'help'})
async def handle_help(message: types.Message, data: dict):
    await message.reply("Сейчас с вами свяжется агент из штаба, боту грустно, что он непонятный:(")


@dp.message_handler(payload={"command": 'marks'})
async def handle_marks(message: types.Message, data: dict):
    await message.reply("Тут будут баллы команды.")


@dp.message_handler(rules.Command("admin"), IsAdmin(True))
async def admin_panel(message: types.Message, data: dict):
    USERS[message.from_id] = 'user_choose'
    await message.reply("You now is user_choose! \U0001f600", keyboard=kb_admin.get_keyboard())


@dp.message_handler(rules.Command("teams"), IsAdmin(True))
async def admin_list_of_teams(message: types.Message, data: dict):
    await message.reply("Print list of teams to admin")


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


@dp.message_handler(IsLeadChoose(True))  # обработка названий команды. TODO: машина состояний
async def handle_lead_chooses_team_name(message: types.Message, data: dict):
    USERS[message.from_id] = "lead"
    TEAMS[message.from_id] = message.text
    LEADS[message.from_id] = message.from_id  # сам себе капитан
    await message.answer("Ура, команда %s зарегистрирована!\nЧтобы члены твоей команды смогли к тебе присоединиться, "
                         "пусть напишут мне этот код: \n%s" % (TEAMS[message.from_id], message.from_id),
                         keyboard=kb_main.get_keyboard())


@dp.message_handler(IsUserChoose(True))  # обработка названий команды
async def handle_user_choose_team(message: types.Message, data: dict):
    if int(message.text) in USERS:
        if USERS[int(message.text)] == 'lead':
            LEADS[message.from_id] = message.text
            USERS[message.from_id] = 'user'
            await message.answer("Отлично, теперь вы член команды %s. Бегом в игру!" % int(message.text),
                                 keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Перепроверь, у капитана точно %s? Если не поможет, пиши в помощь" % message.text)
    else:
        await message.answer("Перепроверь, у капитана точно %s? Напиши мне точно!" % message.text)


@dp.message_handler(IsNew(True))  # если клавы не сработают
async def get_start_message(message: types.Message, data: dict):
    await message.reply("Привет! Космический рейс в лице бота Афанасия приветствует тебя!\n"
                        "Капитан должен зарегистрировать команду. "
                        "Как только он закончит, присоединяйтесь к нему и бегом в игру!",
                        keyboard=kb_choose.get_keyboard())


async def run():
    dp.run_polling()


if __name__ == "__main__":
    dp.setup_middleware(RegistrationMiddleware())  # setup middleware
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
