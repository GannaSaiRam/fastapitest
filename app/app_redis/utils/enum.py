from enum import Enum


class Status(str, Enum):
    SCHEDULED = 'SCHEDULED'
    STARTED = "STARTED"
    PENDING = "PENDING"
    IN_PROCESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
