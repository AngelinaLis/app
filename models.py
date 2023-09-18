from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    start_time = Column(DateTime, default=datetime.now().strftime("%m.%d.%Y, %H:%M:%S"))
    change_time = Column(DateTime)
    notes = relationship("Note", backref="board")


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)
    start_time = Column(DateTime, default=datetime.now().strftime("%m.%d.%Y, %H:%M:%S"))
    change_time = Column(DateTime)
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)
