from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# структура базы:
# table GENERAL
# user_id|name|riddle1|key1|riddle2|key2|riddle3|key3|...|riddle10|key10|photo1|photo2|photo3
# 192168 |лупа|0-10   |8931|


class General(Base):  # Когда капитан вводит название команды, генерируется строка этой таблицы и таблицы CommandNames
    __tablename__ = 'GENERAL'
    id = Column(Integer, primary_key=True)
    captain_id = Column(String(255))
    command_name = Column(String(255))
    r1 = Column(Integer)  # mark for solving - 0 to 15 ISZ
    k1 = Column(Integer)
    r2 = Column(Integer)  # Prokhodnaya RKK
    k2 = Column(Integer)
    r3 = Column(Integer)  # Mozzhorin
    k3 = Column(Integer)
    r4 = Column(Integer)  # Lunodrom
    k4 = Column(Integer)
    r5 = Column(Integer)  # kolledzh dvigateli
    k5 = Column(Integer)
    r6 = Column(Integer)  # raketa u IPK Mashpribor
    k6 = Column(Integer)
    r7 = Column(Integer)  # Besedka LUNA
    k7 = Column(Integer)
    r8 = Column(Integer)  # pamyatnik korollevu na prospekte
    k8 = Column(Integer)
    r9 = Column(Integer)  # pamyatnik Isaevu
    k9 = Column(Integer)
    r10 = Column(Integer)  # Pushka Grabina
    k10 = Column(Integer)
    r11 = Column(Integer)  # kovorking
    k11 = Column(Integer)
    r12 = Column(Integer)  # LES antikafe
    k12 = Column(Integer)
    r13 = Column(Integer)  # кванториум
    k13 = Column(Integer)
    r14 = Column(Integer)  # краеведческий музей
    k14 = Column(Integer)
    p1 = Column(Integer)  # по 5 баллов за фотозадания
    p2 = Column(Integer)
    p3 = Column(Integer)
    p4 = Column(Integer)
    p5 = Column(Integer)


class CommandNames(Base):  # капитан создал - участники команды при вводе названия команды ищут по названию айди
    __tablename__ = 'COMMANDNAMES'  # (нулл - варнинг) и, найдя его, делают новую запись айди команды - свой айди
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255))
    command_id = Column(String(255))


class Agents(Base):  # кмк, агенты должны сами о себе заявить. Ну а хули
    __tablename__ = 'AGENTS'  # ну и у админа будет команда "айди номер этапа" чтобы дать челибосу админку
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255))
    stage_id = Column(String(255))  # от 1 до 14
