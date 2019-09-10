from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# структура базы:
# table GENERAL
# user_id|name|riddle1|key1|riddle2|key2|riddle3|key3|...|riddle10|key10|photo1|photo2|photo3
# 192168 |лупа|0-10   |8931|


class General(Base):
    __tablename__ = 'general'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255))
    name = Column(String(255))
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
    r13 = Column(Integer)  # Kvantorium
    k13 = Column(Integer)
    r14 = Column(Integer)  # Kraevedcheskiy muzey
    k14 = Column(Integer)
    p1 = Column(Integer)  #po 5 ballov za fotozadaniya
    p2 = Column(Integer)
    p3 = Column(Integer)
    p4 = Column(Integer)
    p5 = Column(Integer)
