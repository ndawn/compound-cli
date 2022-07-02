from enum import Enum

from sqlalchemy import Column
from sqlalchemy import Enum as EnumField
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class CompoundType(Enum):
    ADP = 'ADP'
    ATP = 'ATP'
    STI = 'STI'
    ZID = 'ZID'
    DPM = 'DPM'
    XP9 = 'XP9'
    O8W = '18W'
    T9P = '29P'


class Compound(Base):
    __tablename__ = 'compounds'
    __table_args__ = (UniqueConstraint('name', 'type', 'formula', 'inchi', 'inchi_key', 'smiles'),)

    id: int = Column(Integer, primary_key=True)
    type: CompoundType = Column(EnumField(CompoundType))
    name: str = Column(String(255))
    formula: str = Column(String(255))
    inchi: str = Column(Text)
    inchi_key: str = Column(String(255))
    smiles: str = Column(String(255))
    cross_links_count: int = Column(Integer)
