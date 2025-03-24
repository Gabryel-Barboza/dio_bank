from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    pass
