from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from app.db.database import Base


class Feedback(Base):

    __tablename__ = "feedback"

    id = Column(
        Integer,
        primary_key=True
    )

    question = Column(Text)

    answer = Column(Text)

    rating = Column(Integer)