from models import BatchJobEventDetails, BatchJobEventDetailsSeq
from crud.crud_base import CRUDBase


class BatchJobEventDetailsCRUD(CRUDBase):
    def __init__(self):
        super().__init__(BatchJobEventDetails, BatchJobEventDetailsSeq)
