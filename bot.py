import logging
from vk import types
from vk.bot_framework import BaseRule, BaseMiddleware, rules
from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher
from vk.bot_framework import Storage
import emoji  # https://www.webfx.com/tools/emoji-cheat-sheet/
#from sets import Set

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
        '1a': ['исз', 'спутник', 'искусственный спутник земли', 'первый спутник'],
        2: 'Тут ещё легенда не готова. Либо тыкай НАЗАД, либо ответ РКК))))',
        '2a': ['ркк'],
        3: 'Сыграем в мини-версию игры \"морской бой\"? Формат ввода координат: А1.\n'
           'На поле находится 3 корабля (1 - Трехпалубный, 2 - Однопалубных). '
           'Эти корабли дают название места, где находится этап.',
        '3a': set(['к2', "к3", "к4", "м6", 'т9']),
        4: 'Как будет загадан этап: так же что и у лунодрома. Либо жмии НАЗАД, либо ответ ПУСК',
        '4a': ['пуск'],
        5: 'Только представьте, а что если бы можно было перенестись в прошлое и стать свидетелями диалога этих двух '
           'выдающихся людей? Вот сидят они в сквере, который позже будет носить громкий титул одного из них, '
           'и ведут неспешную беседу: «Как приятно вот так сесть и поговорить по душам, а, Юр?». Агентов не трогать!'
           'Овтетом будет желтое изображение на фасаде здания у этапа в формате: “******”',
        '5a': ['звезды', 'звезда'],
        6: 'Я очень люблю путешествия, ведь так прекрасно сесть поздно вечером и просто понаблюдать. \n'
           '1. В Ташкенте я смотрел на Волосы Вероники, Деву, Льва, потом на Деву, Насос, снова на Деву и Волка.\n'
           '2. В Хаммерфест я смотрел на Рысь, Жирафа, Лиру, Голову змеи и снова на Рысь.\n'
           '3. В Афинах я смотрел на Корму, Зайца и Голубя.\n'
           '4. В Малаге я смотрел на Секстант, Рака и Единорога.\n'
           '5. В Катманду я смотрел на Корму, Зайца, Сетку, Резец, Голубя и Корму.\n'
           '6. В Сиднее я смотрел на Кита, Треугольник, Лисичку и Орла.\n'
           '7. В Мумбаи я смотрел на Чашу, Весы, Волка и  Насос.\n'
           'Пришли мне агаданное слово в формате: *******',
        '6a': ['коллапс'],
        7: 'Все любят получать подарки на память, и участники нашего квеста не исключение. На одном из предметов, '
           'который очень любит свет, загадано место следующего этапа. '
           'Агенты ждут у памятника, восточнее загаданного объекта. '
           'Ответом будет количество опор у загаданного объекта.',
        '7a': ['3', 'три'],
        8: 'На главном проспекте города, на участке от 3 до 5 дома, ходит специальный человек. Найдите его, выполните '
           'его небольшое задание и он укажет место этапа. ',
        '8a': ['загс'],
        9: 'Профессор, доктор технических наук. Умер в Калининграде в 1980 году. В городе стоит его детище с 100 '
           'размером, агенты ждут там. Ответом будет индекс ГАУ загаданного объекта в формате: **-*-***.',
        '9a': ['52-П-412'],
        10: 'Это задание для вас подготовил космонавт А.А. Иванов. Чтобы узнать вопрос, перейдите по ссылке на видео: '
            'ссылка',
        '10a': ['ссылка'],
        11: 'У вас есть уникальная возможность выиграть в нашей лотерее. Сотрите защитный слой билета, который '
            'находится в конверте, и отправляйтесь к агентам. Ответом будет название загаданного места в формате: '
            '******** (возможны и другие варианты написания).',
        '11a': ['лес', 'антикафе', 'антикафе лес'],
        12: 'Королев, город с богатой и интересной историей. Разгадайте этот  кроссворд, и он укажет место следующего '
            'этапа:\n'
            '1. Ферма станции "Мир".\n'
            '2. Модуль станции "Мир".\n'
            '3. Самый известный продукт г. Королёв.\n'
            '4. Модуль станции "Мир", состоящий из двух отсеков, пригодных для работы экипажа, и одного аппаратного '
            'отсека.\n'
            '5. Название ракеты запущенной 12 апреля 1961 г.\n'
            '6. Самый главный заказчик продукции Королёва (аббревиатура).\n'
            '7. Город основанный в 1938 г.\n'
            '8. Разработчик “Лапоток”.\n'
            '9. В честь него названы сквер и улица возле главного градообразующего предприятия.\n'
            '10. Невелик и не мал для "Газпрома".',
        '12a': ['флуктуация']}

USERS = {}  # schema - id: lead, user, agent, lead_choose, user_choose, new
TEAMS = {}  # schema - team_id: team_name
LEADS = {}  # schema - id: lead_id=team_id
MARKS = {}  # schema - team_id: {1:0,2:}
AGENTS = {}  # schema - id: stage
PROGRESS = {}  # schema - id_lead: 1..10 idle
SEA_WAR = {}  # schema - id_lead: Set(['точки МБ','точки '])
SEA_WAR_PRINT = {}  # schema - id_lead: [t0, t1, t2...]
t0 = '\u3000И\u3000К\u3000Л\u3000М\u3000Н\u3000О\u3000П\u3000Р\u3000С\u3000Т\n'
t1 = '1\n'
t2 = '2\n'
t2_solved = '2 \u3000 \U0001F4A5\n'
t2_killed = '2 \u3000 \U0001F480\n'
t3 = '3\n'
t3_solved = '3 \u3000 \U0001F4A5\n'
t3_killed = '3 \u3000 \U0001F480\n'
t4 = '4\n'
t4_solved = '4 \u3000 \U0001F4A5\n'
t4_killed = '4 \u3000 \U0001F480\n'
t5 = '5\n'
t6 = '6\n'
t6_solved = '6 \u3000\u3000\u3000\u3000\u3000\U0001F480\n'
t7 = '7\n'
t8 = '8\n'
t9 = '9\n'
t9_solved = '9\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\U0001F480\n'
t10 = '10'
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
    await message.reply(t0)


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


@dp.message_handler(payload={"command": 'kb_back_to_main'})
async def handle_off_riddle(message: types.Message, data: dict):
    PROGRESS[message.from_id] = 'idle'
    USERS[message.from_id] = 'lead'
    await message.reply("Хорошо",
                        keyboard=kb_main.get_keyboard())


@dp.message_handler(IsSolving(True))  # TODO: учёт баллов
async def handle_solving(message: types.Message, data: dict):
    if PROGRESS[message.from_id] == '1':
        if message.text.lower() in TEXT['1a']:
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            MARKS[message.from_id][1] = 5
            await message.answer("Верно! Вы получили 5 баллов за верное решение. Бегом искать точку и решать задание "
                                 "агента - там ещё 10 баллов!", keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Нет, попробуй другой ответ. Может, аббревиатуру. Или жми кнопку снизу, позже "
                                 "вернёшься к этой задаче",
                                 keyboard=kb_back_to_main.get_keyboard())
    elif PROGRESS[message.from_id] == '2':
        if message.text.lower() in TEXT['2a']:
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            MARKS[message.from_id][2] = 5
            await message.answer("Верно! Вы получили 5 баллов за верное решение второго задания. Бегом искать точку и "
                                 "решать задание агента - там ещё 10 баллов!", keyboard=kb_main.get_keyboard())
        else:
            await message.answer('Нет, попробуй другой ответ. Или жми кнопку снизу, позже вернёшься к этой задаче',
                                 keyboard=kb_back_to_main.get_keyboard())
    elif PROGRESS[message.from_id] == '3':  # SEA_WAR SEA_WAR_PRINT
        if message.text.lower() == 'кккмт' or message.text.lower() == '3кмт':
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            MARKS[message.from_id][3] = 5  # - place in !!! only int
            await message.answer(
                "Верно! Вы получили 5 баллов за верное решение. Бегом искать точку и решать задание "
                "агента - там ещё 10 баллов!", keyboard=kb_main.get_keyboard())
        elif message.text.lower() in TEXT['3a']:
            if message.text.lower() == 'к2':  # k2 k3 k4 m6 t9
                SEA_WAR[message.from_id][2] = t2_solved
                SEA_WAR_PRINT[message.from_id].add('к2')
            elif message.text.lower() == 'к3':
                SEA_WAR[message.from_id][3] = t3_solved
                SEA_WAR_PRINT[message.from_id].add('к3')
            elif message.text.lower() == 'к4':
                SEA_WAR[message.from_id][4] = t4_solved
                SEA_WAR_PRINT[message.from_id].add('к4')
            elif message.text.lower() == 'м6':
                SEA_WAR[message.from_id][6] = t6_solved
                SEA_WAR_PRINT[message.from_id].add('м6')
            elif message.text.lower() == 'т9':
                SEA_WAR_PRINT[message.from_id].add('т9')
                SEA_WAR[message.from_id][9] = t9_solved
            if SEA_WAR[message.from_id][2] == t2_solved and SEA_WAR[message.from_id][3] == t3_solved and SEA_WAR[message.from_id][4] == t4_solved:
                SEA_WAR[message.from_id][2] = t2_killed
                SEA_WAR[message.from_id][3] = t3_killed
                SEA_WAR[message.from_id][4] = t4_killed
            await message.answer('Попал!\n' + SEA_WAR[message.from_id][0] + SEA_WAR[message.from_id][1] +
                                 SEA_WAR[message.from_id][2] + SEA_WAR[message.from_id][3] + SEA_WAR[message.from_id][
                                     4] +
                                 SEA_WAR[message.from_id][5] + SEA_WAR[message.from_id][6] + SEA_WAR[message.from_id][
                                     7] +
                                 SEA_WAR[message.from_id][8] + SEA_WAR[message.from_id][9] + SEA_WAR[message.from_id][
                                     10],
                                 keyboard=kb_back_to_main.get_keyboard())
            if SEA_WAR_PRINT[message.from_id] == TEXT['3a']:
                await message.answer(
                    "Ты потопил все мои корабли. Теперь отгадай кодовое слово и назови его мне! Это аббревиатура. Если "
                    "никак не получается, нажми кнопку снизу и зови на помощь",
                    keyboard=kb_back_to_main.get_keyboard())
        else:
            await message.answer("Мимо!", keyboard=kb_back_to_main.get_keyboard())
    elif PROGRESS[message.from_id] == '4':
        if message.text.lower() in TEXT['4a']:
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            MARKS[message.from_id][4] = 5
            await message.answer("Верно! Вы получили 5 баллов за верное решение четвёртого задания."
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов!",
                                 keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Нет, попробуй другой ответ. Или жми кнопку снизу, позже вернёшься к этой задаче",
                                 keyboard=kb_back_to_main.get_keyboard())
    elif PROGRESS[message.from_id] == '5':
        if message.text.lower() in TEXT['5a']:
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            MARKS[message.from_id][5] = 5
            await message.answer("Верно! Вы получили 5 баллов за верное решение пятого задания."
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов!",
                                 keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Нет, попробуй другой ответ. Или жми кнопку снизу, позже вернёшься к этой задаче",
                                 keyboard=kb_back_to_main.get_keyboard())
    elif PROGRESS[message.from_id] == '6':
        if message.text.lower() in TEXT['6a']:
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            MARKS[message.from_id][6] = 5
            await message.answer("Верно! Вы получили 5 баллов за верное решение шестого задания."
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов!",
                                 keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Нет, попробуй другой ответ. Или жми кнопку снизу, позже вернёшься к этой задаче",
                                 keyboard=kb_back_to_main.get_keyboard())
    elif PROGRESS[message.from_id] == '7':
        if message.text.lower() in TEXT['7a']:
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            MARKS[message.from_id][7] = 5
            await message.answer("Верно! Вы получили 5 баллов за верное решение седьмого задания."
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов!",
                                 keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Нет, попробуй другой ответ. Или жми кнопку снизу, позже вернёшься к этой задаче",
                                 keyboard=kb_back_to_main.get_keyboard())
    elif PROGRESS[message.from_id] == '8':
        if message.text.lower() in TEXT['8a']:
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            MARKS[message.from_id][8] = 5
            await message.answer("Верно! Вы получили 5 баллов за верное решение восьмого задания."
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов!",
                                 keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Нет, попробуй другой ответ. Или жми кнопку снизу, позже вернёшься к этой задаче",
                                 keyboard=kb_back_to_main.get_keyboard())
    elif PROGRESS[message.from_id] == '9':
        if message.text.lower() in TEXT['9a']:
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            MARKS[message.from_id][9] = 5
            await message.answer("Верно! Вы получили 5 баллов за верное решение девятого задания."
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов!",
                                 keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Нет, попробуй другой ответ. Или жми кнопку снизу, позже вернёшься к этой задаче",
                                 keyboard=kb_back_to_main.get_keyboard())
    elif PROGRESS[message.from_id] == '10':
        if message.text.lower() in TEXT['10a']:
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            MARKS[message.from_id][10] = 5
            await message.answer("Верно! Вы получили 5 баллов за верное решение десятого задания."
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов!",
                                 keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Нет, попробуй другой ответ. Или жми кнопку снизу, позже вернёшься к этой задаче",
                                 keyboard=kb_back_to_main.get_keyboard())
    elif PROGRESS[message.from_id] == '11':
        if message.text.lower() in TEXT['11a']:
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            MARKS[message.from_id][11] = 5
            await message.answer("Верно! Вы получили 5 баллов за верное решение одиннадцатого задания."
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов!",
                                 keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Нет, попробуй другой ответ. Или жми кнопку снизу, позже вернёшься к этой задаче",
                                 keyboard=kb_back_to_main.get_keyboard())
    elif PROGRESS[message.from_id] == '12':
        if message.text.lower() in TEXT['12a']:
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            MARKS[message.from_id][12] = 5
            await message.answer("Верно! Вы получили 5 баллов за верное решение двенадцатого задания."
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов!",
                                 keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Нет, попробуй другой ответ. Или жми кнопку снизу, позже вернёшься к этой задаче",
                                 keyboard=kb_back_to_main.get_keyboard())
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
    if USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '2'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[2], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[2], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="3")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_3_riddle(message: types.Message, data: dict):
    if USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '3'
        USERS[message.from_id] = 'solving'
        SEA_WAR[message.from_id] = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]
        SEA_WAR_PRINT[message.from_id] = set()
        await message.answer(TEXT[3] + '\n' + SEA_WAR[message.from_id][0] + SEA_WAR[message.from_id][1] +
                             SEA_WAR[message.from_id][2] + SEA_WAR[message.from_id][3] + SEA_WAR[message.from_id][4] +
                             SEA_WAR[message.from_id][5] + SEA_WAR[message.from_id][6] + SEA_WAR[message.from_id][7] +
                             SEA_WAR[message.from_id][8] + SEA_WAR[message.from_id][9] + SEA_WAR[message.from_id][10],
                             keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[3], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="4")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_4_riddle(message: types.Message, data: dict):
    if USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '4'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[4], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[4], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="5")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_5_riddle(message: types.Message, data: dict):
    if USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '5'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[5], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[5], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="6")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_6_riddle(message: types.Message, data: dict):
    if USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '6'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[6], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[6], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="7")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_7_riddle(message: types.Message, data: dict):
    if USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '7'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[7], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[7], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="8")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_8_riddle(message: types.Message, data: dict):
    if USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '8'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[8], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[8], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="9")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_9_riddle(message: types.Message, data: dict):
    if USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '9'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[9], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[9], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="10")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_10_riddle(message: types.Message, data: dict):
    if USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '10'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[10], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[10], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="11")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_11_riddle(message: types.Message, data: dict):
    if USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '11'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[11], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[11], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="12")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_12_riddle(message: types.Message, data: dict):
    if USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '12'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[12], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[12], keyboard=kb_main.get_keyboard())


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
