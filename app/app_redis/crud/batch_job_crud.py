from models import BatchJob, BatchJobSeq
from crud.crud_base import CRUDBase


class BatchJobCRUD(CRUDBase):
    def __init__(self):
        super().__init__(BatchJob, BatchJobSeq)
