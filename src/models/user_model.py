from sqlmodel import Field, SQLModel


# TODO: date type para birth_date
# Modelo base, se comporta como uma interface
class UserBaseModel(SQLModel):
    # Tipo TEXT para SQLite e VARCHAR(255) para MySQL, apenas VARCHAR para outros
    name: str = Field(index=True)
    address: str | None = Field(default=None)
    cpf: str = Field(index=True, min_length=11, max_length=11)
    birth_date: str | None = Field(default=None)
    password: str = Field(default='123')


# Modelo para criar tabelas
class User(UserBaseModel, table=True):
    # Type hint == attribute type, None == nullable

    # Valor padrão None/Null, caso contrário ainda será necessário passar o dado na instância
    # Gerado pelo database, não pela instância
    id_user: int | None = Field(default=None, primary_key=True)


# Modelo com atributos necessários para criar um usuário
class UserCreateModel(UserBaseModel):
    pass


# Modelo com atributos para atualizar um usuário com Patch
class UserUpdateModel(UserBaseModel):
    name: str | None
    cpf: str | None
    password: str | None


# Modelo com os atributos obrigatórios que são retornados para o cliente
class UserPublicModel(UserBaseModel):
    id_user: int
    address: str
    birth_date: str
