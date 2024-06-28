from models import BatchJobEvents, BatchJobEventsSeq
from crud.crud_base import CRUDBase


class BatchJobEventsCRUD(CRUDBase):
    def __init__(self):
        super().__init__(BatchJobEvents, BatchJobEventsSeq)
