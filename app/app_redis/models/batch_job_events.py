from sqlalchemy import Integer, String, Sequence
from sqlalchemy.orm import relationship, mapped_column

from config import TABLE_NAMES
from models.base import Base


class BatchJobEvents(Base):
    __table_args__ = {"schema": TABLE_NAMES["SCHEMAS"][2]}
    __tablename__ = TABLE_NAMES["TABLES"][2]

    batch_job_id = mapped_column(Integer, nullable=True)
    event = mapped_column(String(100), nullable=False)
    status = mapped_column(String(50), nullable=False)


BatchJobEventsSeq = Sequence(TABLE_NAMES["SEQUENCES"][2], quote=False)
