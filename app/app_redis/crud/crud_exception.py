from psycopg2.errorcodes import UNIQUE_VIOLATION, FOREIGN_KEY_VIOLATION
from psycopg2.errors import lookup

UniqueViolation = lookup(UNIQUE_VIOLATION)
ForeignKeyViolation = lookup(FOREIGN_KEY_VIOLATION)


class CRUDException(Exception):
    def __init__(self, message, *args, **_):
        super().__init__(*args)
        self.message = str(message)


class CRUDUniqueViolation(CRUDException):
    def __str__(self):
        return f"Violates unique key constraint: {self.message}"


class CRUDForeignKeyViolation(CRUDException):
    def __str__(self):
        return f"Violates foreign key constraint: {self.message}"


class CRUDExceptionFactory:
    @classmethod
    def get_exception(cls, e):
        if isinstance(e.orig, UniqueViolation):
            raise CRUDUniqueViolation(e)
        elif isinstance(e.orig, ForeignKeyViolation):
            raise CRUDForeignKeyViolation(e)
        else:
            raise CRUDException(e)
