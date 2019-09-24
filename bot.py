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

TEXT = {1: 'Памятник загадан с помощью AR-приложения. Ссылка на его скачивание, если вы не сделали этого заранее: '
           'https://play.google.com/store/apps/details?id=ru.izobretarium.app.spacear',
        '1a': ['ИСЗ', 'спутник', 'искусственный спутник земли'],
        2: 'Современное наименование предприятие получило в 1994 г. До этого было известно как отдел 3 СКБ НИИ-88, '
           'Особое конструкторское бюро-1 (ОКБ-1), Центральное конструкторское бюро экспериментального машиностроения '
           '(ЦКБЭМ), Научно-производственное объединение (НПО) \"Энергия\".'
           ' При головной роли предприятия в последующие '
           'годы созданы: \n орбитальные станции «Салют» (1971); «Салют-4» (1974-1977); «Салют-6» (1977-1982); '
           '«Салют-7» (1982-1991); многомодульная станция «Мир» (1986-2001), ставшая первым международным '
           'исследовательским космическим центром, на котором выполнялись проекты "Евромир", "Мир-Шаттл", "Мир-НАСА";'
           ' Российский сегмент Международной космической станции (с 1998); пилотируемые космические корабли'
           ' «Союз» (1966-1981), «Союз Т» (1979-1986), «Союз ТМ» (1986-2002), «Союз ТМА» (2002-2012), «Союз ТМА-М» '
           '(2010-2016), «Союз МC» (с 2016); грузовые космические корабли «Прогресс» (1978-1990), «Прогресс М» '
           '(1989-2009), «Прогресс М1» (2000-2004), «Прогресс М-М» (2008-2015), «Прогресс МС» (с 2015); многоразовая '
           'космическая система «Энергия–Буран» с крупнейшей в мире ракетой-носителем «Энергия» (1987), которая до '
           'настоящего времени не имеет технических аналогов в мире, и многоразовым ОК «Буран» (1988); космическая '
           'орбитальная обсерватория «Гамма» астрофизического и геофизического направлений (1990-1992); спутники связи '
           'нового поколения «Ямал-100» (1999-2011), «Ямал-200» (с 2003); спутник дистанционного зондирования Земли '
           '(ДЗЗ) «БелКА» (2006); космическая система ДЗЗ для иностранного заказчика (2014-2015) и др. Предприятие '
           'являлось активным участником международных космических программ: \"Союз-Аполлон\", \"Интеркосмос\".',
        '2a': [],
        3: 'third задание',
        4: 'fourth задание'}

USERS = {}  # schema - id: lead, user, agent, lead_choose, user_choose, new
TEAMS = {}  # schema - team_id: team_name
LEADS = {}  # schema - id: lead_id=team_id
MARKS = {}  # schema - team_id: {1:0,2:}
AGENTS = {}  # schema - id: stage
PROGRESS = {}  # schema - id_lead: 1..10 idle
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


class IsSolving(BaseRule):
    """
    Проверка статуса капитана
    """

    def __init__(self, is_admin: bool):
        self.is_admin: bool = is_admin

    async def check(self, message: types.Message, data: dict):
        status = USERS[message.from_id]
        if not self.is_admin and status != "solving":
            return True
        elif not self.is_admin and status == "solving":
            return False
        elif self.is_admin and status == "solving":
            return True
        elif self.is_admin and status != "solving":
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


class IsAgent(BaseRule):
    """
    Проверка статуса агента
    """

    def __init__(self, is_admin: bool):
        self.is_admin: bool = is_admin

    async def check(self, message: types.Message, data: dict):
        status = USERS[message.from_id]
        if not self.is_admin and status != "agent":
            return True
        elif not self.is_admin and status == "agent":
            return False
        elif self.is_admin and status == "agent":
            return True
        elif self.is_admin and status != "agent":
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
    await message.reply("You now is in admin mode! \U0001f600", keyboard=kb_admin.get_keyboard())


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


@dp.message_handler(IsSolving(True))  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_solving(message: types.Message, data: dict):
    if PROGRESS[message.from_id] == '1':
        if message.text in TEXT['1a']:
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            await message.answer("Верно!", keyboard=kb_main.get_keyboard())
    else:
        PROGRESS[message.from_id] = 'idle'
        USERS[message.from_id] = 'lead'
        await message.answer("Что-то не так, вернёмся в главное меню", keyboard=kb_back_to_main.get_keyboard())


@dp.message_handler(text="1")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_1_riddle(message: types.Message, data: dict):
    if USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '1'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[1], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[1], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="2")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_2_riddle(message: types.Message, data: dict):
    await message.answer(TEXT[2], keyboard=kb_back_to_main.get_keyboard())


@dp.message_handler(text="3")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_3_riddle(message: types.Message, data: dict):
    await message.answer(TEXT[3], keyboard=kb_back_to_main.get_keyboard())


@dp.message_handler(payload={"command": 'back_to_main'})
async def handle_off_riddle(message: types.Message, data: dict):
    PROGRESS[message.from_id] = 'idle'
    await message.reply("Хорошо",
                        keyboard=kb_main.get_keyboard())


@dp.message_handler(IsLeadChoose(True))  # обработка названий команды. TODO: машина состояний
async def handle_lead_chooses_team_name(message: types.Message, data: dict):
    USERS[message.from_id] = "lead"
    TEAMS[message.from_id] = message.text
    LEADS[message.from_id] = message.from_id  # сам себе капитан
    MARKS[message.from_id] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    await message.answer("Ура, команда %s зарегистрирована!\nЧтобы члены твоей команды смогли к тебе присоединиться, "
                         "пусть напишут мне этот код: \n%s" % (TEAMS[message.from_id], message.from_id),
                         keyboard=kb_main.get_keyboard())


@dp.message_handler(IsUserChoose(True))  # обработка названий команды
async def handle_user_choose_team(message: types.Message, data: dict):
    if int(message.text) in USERS:
        if USERS[int(message.text)] == 'lead':
            LEADS[message.from_id] = message.text
            USERS[message.from_id] = 'user'
            await message.answer("Отлично, теперь вы член команды %s. Бегом в игру!" % TEAMS[int(message.text)],
                                 keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Перепроверь, у капитана точно %s? Если не поможет, пиши в помощь" % message.text)
    else:
        await message.answer("Перепроверь, у капитана точно %s? Напиши мне как у него!" % message.text)


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
