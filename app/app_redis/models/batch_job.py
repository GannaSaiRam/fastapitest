from sqlalchemy import Integer, String, Text, Sequence
from sqlalchemy.orm import relationship, mapped_column

from config import TABLE_NAMES
from models.base import Base


class BatchJob(Base):
    __table_args__ = {"schema": TABLE_NAMES["SCHEMAS"][1]}
    __tablename__ = TABLE_NAMES["TABLES"][1]

    batch_group_id = mapped_column(Integer, nullable=True)
    name = mapped_column(String(250), nullable=False)
    description = mapped_column(Text)
    processing_env = mapped_column(String(50), nullable=False)  # TODO: is this a ENUM? like DEV or PROD
    status = mapped_column(String(50), nullable=False)


BatchJobSeq = Sequence(TABLE_NAMES["SEQUENCES"][1], quote=False)
