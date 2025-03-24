from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    # Type hint == attribute type, None == nullable

    # Valor padrão None/Null, caso contrário ainda será necessário passar o dado na instância
    # Gerado pelo database, não pela instância
    id_usuario: int | None = Field(default=None, primary_key=True)
    # Tipo TEXT para SQLite e VARCHAR(255) para MySQL, apenas VARCHAR para outros
    nome: str = Field(index=True)
    endereco: str | None
    cpf: str
    data_nascimento: str | None
