from sqlmodel import Field, SQLModel


class Account(SQLModel, table=True):
    # Type hint == attribute type, None == nullable
    id_conta: int = Field(default=None, primary_key=True)
    id_usuario: int
    saldo: float
    tipo_conta: str
