from db.base import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


# user_blog = Table("user_blog", Base.metadata,
#                        Column("blog_id", ForeignKey("blog.id"), primary_key=True),
#                        Column("user_id", ForeignKey("user.id"), primary_key=True))


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
    blogs = relationship("Blog",back_populates="author")
