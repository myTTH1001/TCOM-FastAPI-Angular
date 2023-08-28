from db.base import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class FileImage(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    image = Column(String, nullable=False)
