from app.utils.strings import snakecase, to_str
from sqlalchemy import inspect
from sqlalchemy.orm import declared_attr, DeclarativeBase


class BaseModel(DeclarativeBase):
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return snakecase(cls.__name__)

    def __repr__(self):
        identity = inspect(self).identity
        if identity is None:
            pk = "(transient {0})".format(id(self))
        else:
            pk = ', '.join(to_str(value) for value in identity)
        return '<{0} {1}>'.format(type(self).__name__, pk)
