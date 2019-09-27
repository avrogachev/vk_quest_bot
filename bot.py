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
           'https://play.google.com/store/apps/details?id=ru.izobretarium.app.spacear \nНайдите это место в городе,'
           'наведите приложение и получите изображение объекта. Напиши мне, что ты увидел и я скажу, куда идти!',
        '1a': ['исз', 'спутник', 'искусственный спутник земли', 'первый спутник'],
        '1s': 'Что увидел - туда и иди. Внимание! К самому объекту через дорогу не подходите, агенты ждут западнее, у '
              'дома 12',
        2: 'Здесь родилась первая в мире баллистическая ракета межконтинентальной дальности. Здесь создан первый в '
           'мире спутник, первый в мире космический корабль и первая в мире орбитальная станция. С 1946 года и '
           'навсегда — здесь делают космос\nНапиши мне название этого места (я принимаю разные варианты написания)',
        '2a': ['ркк', 'ркк энергия', 'энергия'],
        '2s': 'Идите к той проходной РКК, где вас встречает ракета - там вас встретят агенты',
        3: 'Сыграем в мини-версию игры \"морской бой\"? Формат ввода координат: А1.\n'
           'На поле находится 3 корабля (один трехпалубный, два однопалубных). '
           'Эти корабли дают название места, где находится этап.',
        '3a': set(['к2', "к3", "к4", "м6", 'т9']),
        '3s': 'Идите в КККМТ, там сразу и третий, и четвёртый этап (внутри и снаружи)',
        4: 'Четвёртый этап там же, где и третий - и баллов за нахождение этапа не будет. Отгадывай третью загадку!',
        '4s': 'Четвёртый этап там же, где и третий - реши третью загадку',
        5: 'Только представьте, а что если бы можно было перенестись в прошлое и стать свидетелями диалога этих двух '
           'выдающихся людей? Вот сидят они в сквере, который позже будет носить громкий титул одного из них, '
           'и ведут неспешную беседу: «Как приятно вот так сесть и поговорить по душам, а, Юр?». Агентов не трогать!'
           'Овтетом будет желтое изображение на фасаде здания у этапа в формате: “******”',
        '5a': ['звезды', 'звезда'],
        '5s': 'Агенты ждут в холле “ИПК Машприбор”.',
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
        '6s': 'Этап находится в беседке (Ротонда) “Луна”, что в центральном парке.',
        7: 'Все любят получать подарки на память, и участники нашего квеста не исключение. На одном из предметов, '
           'который очень любит свет, загадано место следующего этапа. '
           'Ответом будет количество опор у загаданного объекта.',
        '7a': ['3', 'три'],
        '7s': 'Агенты ждут у памятника, восточнее загаданного объекта.',
        8: 'На главном проспекте города, на участке от 3 до 5 дома, ходит специальный человек. Найдите его, выполните '
           'его небольшое задание и он укажет место этапа. ',
        '8a': ['ракета'],
        '8s': 'Правильно! Агенты находятся у памятника Исаеву. '
              'Но не торопитесь уходить уходить - если вы найдёте невесту и сделаете с ней командное фото, вы получите'
              ' 3 дополнительных балла за фото с невестой.',   # TODO: захуячить допбаллы за секретные задания
        9: 'Профессор, доктор технических наук. Умер в Калининграде в 1980 году. В городе стоит его детище с 100 '
           'размером, агенты ждут там. Ответом будет индекс ГАУ загаданного объекта в формате: **-*-***.',
        '9a': ['52-п-412'],
        '9s': 'Идите к пушке Грабина, агенты ждут!',
        10: 'Это задание для вас подготовил космонавт А.А. Иванов. Чтобы узнать вопрос, перейдите по ссылке на видео: '
            'ссылка',
        '10a': ['ссылка'],
        '10s': 'Правильно, агенты ждут в Коворкинге по адресу: ул. Грабина, 2Б.',
        11: 'У вас есть уникальная возможность выиграть в нашей лотерее. Сотрите защитный слой билета, который '
            'находится в конверте, и отправляйтесь к агентам. Ответом будет название загаданного места в формате: '
            '******** (возможны и другие варианты написания).',
        '11a': ['лес', 'антикафе', 'антикафе лес'],
        '11s': 'Бегом в Антикафе Лес!',
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
        '12a': ['флуктуация'],
        '12s': 'Агенты ждут внутри “Кванториума”, по адресу ул. Пионерская, д. 34.',
        13: 'В районе проведения квеста есть 5 фото табличек. Фото команды (минимум 3 участника) на фоне таблички - '
            '1 балл.Будьте внимательны - вполне возможно, что таблички попадутся вам по основному маршруту',
        14: 'Если быть пытливыми, то можно получить пару дополнительных заданий и набрать ещё немного баллов:)'}

USERS = {1596791: 'new_agent'  # Ильина
         }  # schema - id: lead, user, agent, lead_choose, user_choose, new
TEAMS = {}  # schema - team_id: team_name
LEADS = {}  # schema - id: lead_id=team_id
MARKS = {}  # schema - team_id: {1:0,2:}
AGENTS = {15967910: '1'  # Ильина
          }  # schema - id: stage
PROGRESS = {}  # schema - id_lead: 1..10 idle
SEA_WAR = {}  # schema - id_lead: Set(['точки МБ','точки '])
SEA_WAR_PRINT = {}  # schema - id_lead: [t0, t1, t2...]
t0 = '\u3000К\u3000Л\u3000М\u3000Н\u3000О\u3000П\u3000Р\u3000С\u3000Т\n'
t1 = '1\n'
t2 = '2\n'
t2_solved = '2 \U0001F4A5\n'
t2_killed = '2 \U0001F480\n'
t3 = '3\n'
t3_solved = '3 \U0001F4A5\n'
t3_killed = '3 \U0001F480\n'
t4 = '4\n'
t4_solved = '4 \U0001F4A5\n'
t4_killed = '4 \U0001F480\n'
t5 = '5\n'
t6 = '6\n'
t6_solved = '6 \u3000 \u3000\u3000\U0001F480\n'
t7 = '7\n'
t8 = '8\n'
t9 = '9\n'
t9_solved = '9\u3000 \u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\U0001F480\n'
t10 = ''
ADMINS = {182840420: 'admin'}

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
        status = USERS[message.from_id]
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


class IsNewAgent(BaseRule):
    """
    Check admin rights of user.
    """

    def __init__(self, is_admin: bool):
        self.is_admin: bool = is_admin

    async def check(self, message: types.Message, data: dict):
        status = USERS[message.from_id]
        if not self.is_admin and status != "new_agent":
            return True
        elif not self.is_admin and status == "new_agent":
            return False
        elif self.is_admin and status == "new_agent":
            return True
        elif self.is_admin and status != "new_agent":
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


class IsAgentChoose(BaseRule):
    """
    Проверка статуса агента
    """

    def __init__(self, is_admin: bool):
        self.is_admin: bool = is_admin

    async def check(self, message: types.Message, data: dict):
        status = USERS[message.from_id]
        if not self.is_admin and status != "agent_choose":
            return True
        elif not self.is_admin and status == "agent_choose":
            return False
        elif self.is_admin and status == "agent_choose":
            return True
        elif self.is_admin and status != "agent_choose":
            return False


class IsAgentMark(BaseRule):
    """
    Проверка статуса агента
    """

    def __init__(self, is_admin: bool):
        self.is_admin: bool = is_admin

    async def check(self, message: types.Message, data: dict):
        status = USERS[message.from_id]
        if not self.is_admin and status != "agent_mark":
            return True
        elif not self.is_admin and status == "agent_mark":
            return False
        elif self.is_admin and status == "agent_mark":
            return True
        elif self.is_admin and status != "agent_mark":
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


@dp.message_handler(IsNewAgent(True))
async def handle_new_agent(message: types.Message, data: dict):
    if message.from_id in AGENTS:
        USERS[message.from_id] = 'agent'
        await message.reply("Приветствую, агент! У тебя уже указан %s этап. По кнопке Список команд - команды, "
                            "получившие хоть какие-то баллы за этот этап. Если там 5 баллов, они отгадали загадку и "
                            "идут к тебе. Если загадку не отгадали - смело шли их отгадывать и не приходить, пока не "
                            "отгадают. Если надо поменять этап или что-то не так, жми копку ПОМОЩЬ, я приду" %
                            AGENTS[message.from_id],
                            keyboard=kb_agent.get_keyboard())
    else:
        USERS[message.from_id] = 'agent_choose'
        await message.reply('Приветствую, агент! Пришли мне цифру своего этапа, у меня не написано, где ты стоишь',
                            keyboard=kb_agent.get_keyboard())


@dp.message_handler(IsAgentChoose(True))
async def handle_agent_choose(message: types.Message, data: dict):
    USERS[message.from_id] = 'agent'
    AGENTS[message.from_id] = message.text
    await message.reply("Приветствую, агент! Теперь у тебя указан %s этап. По кнопке Список команд - команды, "
                        "получившие хоть какие-то баллы за этот этап. Если там 5 баллов, они отгадали загадку и "
                        "идут к тебе. Если загадку не отгадали - смело шли их отгадывать и не приходить, пока не "
                        "отгадают. Если надо поменять этап или что-то не так, жми копку ПОМОЩЬ, я приду" %
                        AGENTS[message.from_id],
                        keyboard=kb_agent.get_keyboard())


@dp.message_handler(payload={"command": 'agent_back'})  # агент послал команду и не стал оценивать
async def handle_agent_mark_back(message: types.Message, data: dict):
    USERS[message.from_id] = 'agent'
    PROGRESS[message.from_id] = 'idle'
    await message.answer("Хорошо, оценим позже", keyboard=kb_agent.get_keyboard())


@dp.message_handler(IsAgentMark(True))
async def handle_agent_mark(message: types.Message, data: dict):
    MARKS[PROGRESS[message.from_id]][int(AGENTS[message.from_id])] = 5 + int(message.text)
    USERS[message.from_id] = 'agent'
    # PROGRESS[message.from_id] = 'idle'
    await message.answer("У команды %s за этот этап в сумме %d "
                         "баллов!" % (TEAMS[PROGRESS[message.from_id]],
                                      MARKS[PROGRESS[message.from_id]][int(AGENTS[message.from_id])]),
                         keyboard=kb_agent.get_keyboard())


@dp.message_handler(IsAgent(True))
async def handle_agent_mark_id(message: types.Message, data: dict):
    if int(message.text) in LEADS.values():
        if MARKS[int(message.text)][int(AGENTS[message.from_id])] == 0:
            await message.answer("Эти ребята ещё не решили загадку. Пусть подумают, решат, а потом можно им проводить "
                                 "этап.", keyboard=kb_agent.get_keyboard())
        elif MARKS[int(message.text)][int(AGENTS[message.from_id])] != 0:
            USERS[message.from_id] = "agent_mark"
            PROGRESS[message.from_id] = int(message.text)
            await message.answer("Всё верно, вижу команду %s, сколько баллов? Если ошибёшься, не беда - "
                                 "баллы можно поставить опять и они перепишут старые" % TEAMS[int(message.text)],
                                 keyboard=kb_agent_back.get_keyboard())
        else:
            await message.answer("Какой-то косяк, пиши в помощь" % message.text)
    else:
        await message.answer("Перепроверь, код команды точно %s? Напиши мне как у него! Если что, в чате капитана "
                             "команды вбей id и у него вылезут точные цифры" % message.text,keyboard=kb_agent.get_keyboard())


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
    await message.reply('\n Чтобы решить загадку и увидеть её целиком, пришли мне её номер '
                        '(просто числом, например, 2)\nКогда загадка будет решена, по номеру загадки будет выдаваться '
                        'место, куда надо идти\n'
                        'Ваши баллы в сумме: %d \n'
                        '1. %d\n'
                        '2. %d\n'
                        '3. %d\n'
                        '4. %d\n'
                        '5. %d\n'
                        '6. %d\n'
                        '7. %d\n'
                        '8. %d\n'
                        '9. %d\n'
                        '10. %d\n'
                        '11. %d\n'
                        '12. %d\n'
                        '13. Фотозадания: %d из 5\n'
                        '14. Допзадания %d' % (MARKS[LEADS[message.from_id]][1] + MARKS[LEADS[message.from_id]][2] +
                                               MARKS[LEADS[message.from_id]][3] + MARKS[LEADS[message.from_id]][4] +
                                               MARKS[LEADS[message.from_id]][5] + MARKS[LEADS[message.from_id]][6] +
                                               MARKS[LEADS[message.from_id]][7] + MARKS[LEADS[message.from_id]][8] +
                                               MARKS[LEADS[message.from_id]][9] + MARKS[LEADS[message.from_id]][10] +
                                               MARKS[LEADS[message.from_id]][11] + MARKS[LEADS[message.from_id]][12] +
                                               MARKS[LEADS[message.from_id]][13] + MARKS[LEADS[message.from_id]][14],
                                               MARKS[LEADS[message.from_id]][1], MARKS[LEADS[message.from_id]][2],
                                               MARKS[LEADS[message.from_id]][3], MARKS[LEADS[message.from_id]][4],
                                               MARKS[LEADS[message.from_id]][5], MARKS[LEADS[message.from_id]][6],
                                               MARKS[LEADS[message.from_id]][7], MARKS[LEADS[message.from_id]][8],
                                               MARKS[LEADS[message.from_id]][9], MARKS[LEADS[message.from_id]][10],
                                               MARKS[LEADS[message.from_id]][11], MARKS[LEADS[message.from_id]][12],
                                               MARKS[LEADS[message.from_id]][13], MARKS[LEADS[message.from_id]][14])
                        )


@dp.message_handler(payload={"command": 'help'})  # TODO: написать тут инструкцию по работе с ботом
async def handle_help(message: types.Message, data: dict):
    await message.reply("Сейчас с вами свяжется агент из штаба, боту грустно, что он непонятный:(")


@dp.message_handler(text='id')
async def id(message: types.Message, data: dict):
    await message.reply("%s" % message.from_id)


@dp.message_handler(rules.Command("admin"))
async def admin_panel(message: types.Message, data: dict):
    if message.from_id in ADMINS.keys():
        USERS[message.from_id] = 'admin'
        await message.reply("You now is in admin mode! \U0001f600", keyboard=kb_admin.get_keyboard())
    else:
        await message.reply("ADmin access is closed! \U0001f600")


@dp.message_handler(IsAdmin(True), text='1')
async def admin_add_1(message: types.Message, data: dict):
    PROGRESS[message.from_id] = '1'
    await message.reply("Ща на первый этап агента определим, какой айди? \U0001f600", keyboard=kb_admin.get_keyboard())


@dp.message_handler(IsAdmin(True), text='2')
async def admin_add_2(message: types.Message, data: dict):
    PROGRESS[message.from_id] = '2'
    await message.reply("Ща на второй этап агента определим, какой айди? \U0001f600", keyboard=kb_admin.get_keyboard())


@dp.message_handler(IsAdmin(True), text='3')
async def admin_add_3(message: types.Message, data: dict):
    PROGRESS[message.from_id] = '3'
    await message.reply("Ща на третий этап агента определим, какой айди? \U0001f600", keyboard=kb_admin.get_keyboard())


@dp.message_handler(IsAdmin(True), text='4')
async def admin_add_4(message: types.Message, data: dict):
    PROGRESS[message.from_id] = '4'
    await message.reply("Ща на 4 этап агента определим, какой айди? \U0001f600", keyboard=kb_admin.get_keyboard())


@dp.message_handler(IsAdmin(True), text='5')
async def admin_add_5(message: types.Message, data: dict):
    PROGRESS[message.from_id] = '5'
    await message.reply("Ща на 5 этап агента определим, какой айди? \U0001f600", keyboard=kb_admin.get_keyboard())


@dp.message_handler(IsAdmin(True), text='6')
async def admin_add_6(message: types.Message, data: dict):
    PROGRESS[message.from_id] = '6'
    await message.reply("Ща на 6 этап агента определим, какой айди? \U0001f600", keyboard=kb_admin.get_keyboard())


@dp.message_handler(IsAdmin(True), text='7')
async def admin_add_7(message: types.Message, data: dict):
    PROGRESS[message.from_id] = '7'
    await message.reply("Ща на 7 этап агента определим, какой айди? \U0001f600", keyboard=kb_admin.get_keyboard())


@dp.message_handler(IsAdmin(True), text='8')
async def admin_add_8(message: types.Message, data: dict):
    PROGRESS[message.from_id] = '8'
    await message.reply("Ща на восьмой этап агента определим, какой айди? \U0001f600", keyboard=kb_admin.get_keyboard())


@dp.message_handler(IsAdmin(True), text='9')
async def admin_add_9(message: types.Message, data: dict):
    PROGRESS[message.from_id] = '9'
    await message.reply("Ща на 9 этап агента определим, какой айди? \U0001f600", keyboard=kb_admin.get_keyboard())


@dp.message_handler(IsAdmin(True), text='10')
async def admin_add_10(message: types.Message, data: dict):
    PROGRESS[message.from_id] = '10'
    await message.reply("Ща на 10 этап агента определим, какой айди? \U0001f600", keyboard=kb_admin.get_keyboard())


@dp.message_handler(IsAdmin(True), text='11')
async def admin_add_11(message: types.Message, data: dict):
    PROGRESS[message.from_id] = '11'
    await message.reply("Ща на 11 этап агента определим, какой айди? \U0001f600", keyboard=kb_admin.get_keyboard())


@dp.message_handler(IsAdmin(True), text='12')
async def admin_add_12(message: types.Message, data: dict):
    PROGRESS[message.from_id] = '12'
    await message.reply("Ща на 12 этап агента определим, какой айди? \U0001f600", keyboard=kb_admin.get_keyboard())


@dp.message_handler(IsAdmin(True))
async def admin_assign_agent(message: types.Message, data: dict):
    if PROGRESS[message.from_id] == '1':
        PROGRESS[message.from_id] = 'idle'
        AGENTS[int(message.text)] = '1'
        USERS[int(message.text)] = 'new_agent'
        await message.reply("Окей, %s теперь агент 1 этапа \U0001f600" % message.text, keyboard=kb_admin.get_keyboard())
    elif PROGRESS[message.from_id] == '2':
        PROGRESS[message.from_id] = 'idle'
        AGENTS[int(message.text)] = '2'
        USERS[int(message.text)] = 'new_agent'
        await message.reply("Окей, %s теперь агент 2 этапа \U0001f600" % message.text, keyboard=kb_admin.get_keyboard())
    elif PROGRESS[message.from_id] == '3':
        PROGRESS[message.from_id] = 'idle'
        AGENTS[int(message.text)] = '3'
        USERS[int(message.text)] = 'new_agent'
        await message.reply("Окей, %s теперь агент 3 этапа \U0001f600" % message.text, keyboard=kb_admin.get_keyboard())
    elif PROGRESS[message.from_id] == '4':
        PROGRESS[message.from_id] = 'idle'
        AGENTS[int(message.text)] = '4'
        USERS[int(message.text)] = 'new_agent'
        await message.reply("Окей, %s теперь агент 4 этапа \U0001f600" % message.text, keyboard=kb_admin.get_keyboard())
    elif PROGRESS[message.from_id] == '5':
        PROGRESS[message.from_id] = 'idle'
        AGENTS[int(message.text)] = '5'
        USERS[int(message.text)] = 'new_agent'
        await message.reply("Окей, %s теперь агент 5 этапа \U0001f600" % message.text, keyboard=kb_admin.get_keyboard())
    elif PROGRESS[message.from_id] == '6':
        PROGRESS[message.from_id] = 'idle'
        AGENTS[int(message.text)] = '6'
        USERS[int(message.text)] = 'new_agent'
        await message.reply("Окей, %s теперь агент 6 этапа \U0001f600" % message.text, keyboard=kb_admin.get_keyboard())
    elif PROGRESS[message.from_id] == '7':
        PROGRESS[message.from_id] = 'idle'
        AGENTS[int(message.text)] = '7'
        USERS[int(message.text)] = 'new_agent'
        await message.reply("Окей, %s теперь агент 7 этапа \U0001f600" % message.text, keyboard=kb_admin.get_keyboard())
    elif PROGRESS[message.from_id] == '8':
        PROGRESS[message.from_id] = 'idle'
        AGENTS[int(message.text)] = '8'
        USERS[int(message.text)] = 'new_agent'
        await message.reply("Окей, %s теперь агент 8 этапа \U0001f600" % message.text, keyboard=kb_admin.get_keyboard())
    elif PROGRESS[message.from_id] == '9':
        PROGRESS[message.from_id] = 'idle'
        AGENTS[int(message.text)] = '9'
        USERS[int(message.text)] = 'new_agent'
        await message.reply("Окей, %s теперь агент 9 этапа \U0001f600" % message.text, keyboard=kb_admin.get_keyboard())
    elif PROGRESS[message.from_id] == '10':
        PROGRESS[message.from_id] = 'idle'
        AGENTS[int(message.text)] = '10'
        USERS[int(message.text)] = 'new_agent'
        await message.reply("Окей, %s теперь агент 10 этапа \U0001f600" % message.text, keyboard=kb_admin.get_keyboard())
    elif PROGRESS[message.from_id] == '11':
        PROGRESS[message.from_id] = 'idle'
        AGENTS[int(message.text)] = '11'
        USERS[int(message.text)] = 'new_agent'
        await message.reply("Окей, %s теперь агент 11 этапа \U0001f600" % message.text, keyboard=kb_admin.get_keyboard())
    elif PROGRESS[message.from_id] == '12':
        PROGRESS[message.from_id] = 'idle'
        AGENTS[int(message.text)] = '12'
        USERS[int(message.text)] = 'new_agent'
        await message.reply("Окей, %s теперь агент 12 этапа \U0001f600" % message.text, keyboard=kb_admin.get_keyboard())
    else:
        PROGRESS[message.from_id] = 'idle'
        await message.reply("скидываю прогресс на айдл \U0001f600", keyboard=kb_admin.get_keyboard())


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
                                 "агента - там ещё 10 баллов! " + TEXT['1s'], keyboard=kb_main.get_keyboard())
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
                                 "решать задание агента - там ещё 10 баллов! " + TEXT['2s'], keyboard=kb_main.get_keyboard())
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
                "агента - там ещё 10 баллов! " + TEXT['3s'], keyboard=kb_main.get_keyboard())
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
                    "Ты потопил все мои корабли. Теперь отгадай кодовое слово и назови его мне! Это аббревиатура, "
                    "формат ответа ***** или ****",
                    keyboard=kb_back_to_main.get_keyboard())
        else:
            await message.answer("Мимо!", keyboard=kb_back_to_main.get_keyboard())
    elif PROGRESS[message.from_id] == '5':
        if message.text.lower() in TEXT['5a']:
            PROGRESS[message.from_id] = 'idle'
            USERS[message.from_id] = 'lead'
            MARKS[message.from_id][5] = 5
            await message.answer("Верно! Вы получили 5 баллов за верное решение пятого задания."
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов! " + TEXT['5s'],
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
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов! " + TEXT['6s'],
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
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов! " + TEXT['7s'],
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
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов! " + TEXT['8s'],
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
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов! " + TEXT['9s'],
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
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов! " + TEXT['10s'],
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
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов! " + TEXT['11s'],
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
                                 " Бегом искать точку и решать задание агента - там ещё 10 баллов! " + TEXT['12s'],
                                 keyboard=kb_main.get_keyboard())
        else:
            await message.answer("Нет, попробуй другой ответ. Или жми кнопку снизу, позже вернёшься к этой задаче",
                                 keyboard=kb_back_to_main.get_keyboard())
    else:
        PROGRESS[message.from_id] = 'idle'
        USERS[message.from_id] = 'lead'
        await message.answer("Что-то не так, вернёмся в главное меню", keyboard=kb_back_to_main.get_keyboard())


@dp.message_handler(text="1")
async def handle_1_riddle(message: types.Message, data: dict):
    if MARKS[LEADS[message.from_id]][1] == 5:
        await message.answer(TEXT['1s'], keyboard=kb_main.get_keyboard())
    elif MARKS[LEADS[message.from_id]][1] > 5:
        await message.answer("Ба, да у вас целых %d баллов за эту задачку, решайте другие!" %
                             MARKS[LEADS[message.from_id]][1], keyboard=kb_main.get_keyboard())
    elif USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '1'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[1], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[1], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="2")
async def handle_2_riddle(message: types.Message, data: dict):
    if MARKS[LEADS[message.from_id]][2] == 5:
        await message.answer(TEXT['2s'], keyboard=kb_main.get_keyboard())
    elif MARKS[LEADS[message.from_id]][2] > 5:
        await message.answer("Ба, да у вас целых %d баллов за эту задачку, решайте другие!" %
                             MARKS[LEADS[message.from_id]][2], keyboard=kb_main.get_keyboard())
    elif USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '2'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[2], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[2], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="3")  # TODO: проверка чёпочём решили ли загадку и что там
async def handle_3_riddle(message: types.Message, data: dict):
    if MARKS[LEADS[message.from_id]][3] == 5:
        await message.answer(TEXT['3s'], keyboard=kb_main.get_keyboard())
    elif MARKS[LEADS[message.from_id]][3] > 5:
        await message.answer("Ба, да у вас целых %d баллов за эту задачку, решайте другие!" %
                             MARKS[LEADS[message.from_id]][3], keyboard=kb_main.get_keyboard())
    elif USERS[message.from_id] == 'lead':
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


@dp.message_handler(text="4")
async def handle_4_riddle(message: types.Message, data: dict):
    if MARKS[LEADS[message.from_id]][4] == 5:
        await message.answer(TEXT['4s'], keyboard=kb_main.get_keyboard())
    elif MARKS[LEADS[message.from_id]][4] > 5:
        await message.answer("Ба, да у вас целых %d баллов за эту задачку, решайте другие!" %
                             MARKS[LEADS[message.from_id]][4], keyboard=kb_main.get_keyboard())
    elif USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '4'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[4], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[4], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="5")
async def handle_5_riddle(message: types.Message, data: dict):
    if MARKS[LEADS[message.from_id]][5] == 5:
        await message.answer(TEXT['5s'], keyboard=kb_main.get_keyboard())
    elif MARKS[LEADS[message.from_id]][5] > 5:
        await message.answer("Ба, да у вас целых %d баллов за эту задачку, решайте другие!" %
                             MARKS[LEADS[message.from_id]][5], keyboard=kb_main.get_keyboard())
    elif USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '5'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[5], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[5], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="6")
async def handle_6_riddle(message: types.Message, data: dict):
    if MARKS[LEADS[message.from_id]][6] == 5:
        await message.answer(TEXT['6s'], keyboard=kb_main.get_keyboard())
    elif MARKS[LEADS[message.from_id]][6] > 5:
        await message.answer("Ба, да у вас целых %d баллов за эту задачку, решайте другие!" %
                             MARKS[LEADS[message.from_id]][6], keyboard=kb_main.get_keyboard())
    elif USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '6'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[6], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[6], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="7")
async def handle_7_riddle(message: types.Message, data: dict):
    if MARKS[LEADS[message.from_id]][7] == 5:
        await message.answer(TEXT['7s'], keyboard=kb_main.get_keyboard())
    elif MARKS[LEADS[message.from_id]][7] > 5:
        await message.answer("Ба, да у вас целых %d баллов за эту задачку, решайте другие!" %
                             MARKS[LEADS[message.from_id]][7], keyboard=kb_main.get_keyboard())
    elif USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '7'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[7], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[7], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="8")
async def handle_8_riddle(message: types.Message, data: dict):
    if MARKS[LEADS[message.from_id]][8] == 5:
        await message.answer(TEXT['8s'], keyboard=kb_main.get_keyboard())
    elif MARKS[LEADS[message.from_id]][8] > 5:
        await message.answer("Ба, да у вас целых %d баллов за эту задачку, решайте другие!" %
                             MARKS[LEADS[message.from_id]][8], keyboard=kb_main.get_keyboard())
    elif USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '8'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[8], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[8], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="9")
async def handle_9_riddle(message: types.Message, data: dict):
    if MARKS[LEADS[message.from_id]][9] == 5:
        await message.answer(TEXT['9s'], keyboard=kb_main.get_keyboard())
    elif MARKS[LEADS[message.from_id]][9] > 5:
        await message.answer("Ба, да у вас целых %d баллов за эту задачку, решайте другие!" %
                             MARKS[LEADS[message.from_id]][9], keyboard=kb_main.get_keyboard())
    elif USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '9'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[9], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[9], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="10")
async def handle_10_riddle(message: types.Message, data: dict):
    if MARKS[LEADS[message.from_id]][10] == 5:
        await message.answer(TEXT['10s'], keyboard=kb_main.get_keyboard())
    elif MARKS[LEADS[message.from_id]][10] > 5:
        await message.answer("Ба, да у вас целых %d баллов за эту задачку, решайте другие!" %
                             MARKS[LEADS[message.from_id]][10], keyboard=kb_main.get_keyboard())
    elif USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '10'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[10], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[10], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="11")
async def handle_11_riddle(message: types.Message, data: dict):
    if MARKS[LEADS[message.from_id]][11] == 5:
        await message.answer(TEXT['11s'], keyboard=kb_main.get_keyboard())
    elif MARKS[LEADS[message.from_id]][11] > 5:
        await message.answer("Ба, да у вас целых %d баллов за эту задачку, решайте другие!" %
                             MARKS[LEADS[message.from_id]][11], keyboard=kb_main.get_keyboard())
    if USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '11'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[11], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[11], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="12")
async def handle_12_riddle(message: types.Message, data: dict):
    if MARKS[LEADS[message.from_id]][12] == 5:
        await message.answer(TEXT['12s'], keyboard=kb_main.get_keyboard())
    elif MARKS[LEADS[message.from_id]][12] > 5:
        await message.answer("Ба, да у вас целых %d баллов за эту задачку, решайте другие!" %
                             MARKS[LEADS[message.from_id]][12], keyboard=kb_main.get_keyboard())
    elif USERS[message.from_id] == 'lead':
        PROGRESS[message.from_id] = '12'
        USERS[message.from_id] = 'solving'
        await message.answer(TEXT[12], keyboard=kb_back_to_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[12], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="13")
async def handle_13_riddle(message: types.Message, data: dict):
    if USERS[message.from_id] == 'lead':
        # PROGRESS[message.from_id] = '13'
        # USERS[message.from_id] = 'solving'
        await message.answer(TEXT[13], keyboard=kb_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[13], keyboard=kb_main.get_keyboard())


@dp.message_handler(text="14")
async def handle_14_riddle(message: types.Message, data: dict):
    if USERS[message.from_id] == 'lead':
        # PROGRESS[message.from_id] = '14'
        # USERS[message.from_id] = 'solving'
        await message.answer(TEXT[14], keyboard=kb_main.get_keyboard())
    else:
        await message.answer('Принимаю ответы только от капитана!\n' + TEXT[14], keyboard=kb_main.get_keyboard())


@dp.message_handler(IsLeadChoose(True))  # обработка названий команды.
async def handle_lead_chooses_team_name(message: types.Message, data: dict):
    USERS[message.from_id] = "lead"
    TEAMS[message.from_id] = message.text
    LEADS[message.from_id] = int(message.from_id)  # сам себе капитан
    MARKS[message.from_id] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
    await message.answer("Ура, команда %s зарегистрирована!\nЧтобы члены твоей команды смогли к тебе присоединиться, "
                         "пусть нажмут кнопку \"Я участник\" и напишут мне этот код: \n%s" %
                         (TEAMS[message.from_id], message.from_id),
                         keyboard=kb_main.get_keyboard())


@dp.message_handler(IsUserChoose(True))  # обработка названий команды
async def handle_user_choose_team(message: types.Message, data: dict):
    if int(message.text) in USERS:
        if USERS[int(message.text)] == 'lead':
            LEADS[message.from_id] = int(message.text)
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
