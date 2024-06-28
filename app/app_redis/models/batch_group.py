from sqlalchemy import Integer, String, Date, Sequence
from sqlalchemy.orm import mapped_column

from config import TABLE_NAMES
from models.base import Base


class BatchGroup(Base):
    __table_args__ = {"schema": TABLE_NAMES["SCHEMAS"][0]}
    __tablename__ = TABLE_NAMES["TABLES"][0]

    parent_id = mapped_column(Integer, nullable=True)
    name = mapped_column(String(250), nullable=False)  # TODO: is name unique?
    status = mapped_column(String(50), nullable=False)
    attr_1_key = mapped_column(String(100), nullable=True)
    attr_1_value = mapped_column(String(100), nullable=True)
    attr_2_key = mapped_column(String(100), nullable=True)
    attr_2_value = mapped_column(String(100), nullable=True)
    attr_3_key = mapped_column(String(100), nullable=True)
    attr_3_value = mapped_column(String(100), nullable=True)
    attr_4_key = mapped_column(String(100), nullable=True)
    attr_4_value = mapped_column(String(100), nullable=True)
    attr_5_key = mapped_column(String(100), nullable=True)
    attr_5_value = mapped_column(String(100), nullable=True)
    attr_6_key = mapped_column(String(100), nullable=True)
    attr_6_value = mapped_column(String(100), nullable=True)


BatchGroupSeq = Sequence(TABLE_NAMES["SEQUENCES"][0], quote=False)
