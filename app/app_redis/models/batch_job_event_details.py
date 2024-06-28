from sqlalchemy import Integer, String, Sequence
from sqlalchemy.orm import relationship, mapped_column

from config import TABLE_NAMES
from models.base import Base


class BatchJobEventDetails(Base):
    __table_args__ = {"schema": TABLE_NAMES["SCHEMAS"][3]}
    __tablename__ = TABLE_NAMES["TABLES"][3]

    batch_job_event_id = mapped_column(Integer, nullable=True)
    event = mapped_column(String(100), nullable=False)
    status = mapped_column(String(50), nullable=False)


BatchJobEventDetailsSeq = Sequence(TABLE_NAMES["SEQUENCES"][3], quote=False)
