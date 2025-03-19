from sqlmodel import Date, Field, SQLModel


class User(SQLModel, table=True):
    # Type hint == attribute type, None == nullable
    id_usuario: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    endereco: str | None
    cpf: str
    data_nascimento: str | None
