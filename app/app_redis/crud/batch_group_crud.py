from models import BatchGroup, BatchGroupSeq
from crud.crud_base import CRUDBase


class BatchGroupCRUD(CRUDBase):
    def __init__(self):
        super().__init__(BatchGroup, BatchGroupSeq)
