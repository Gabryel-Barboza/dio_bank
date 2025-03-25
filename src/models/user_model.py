from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .account_model import Account, AccountPublicModel


# Modelo base, se comporta como uma interface
class UserBaseModel(SQLModel):
    # Tipo TEXT para SQLite e VARCHAR(255) para MySQL, apenas VARCHAR para outros
    fullname: str
    username: str = Field(index=True, max_length=50)
    address: str | None = Field(default=None)
    cpf: str = Field(index=True, min_length=11, max_length=11)
    birth_date: date | None = Field(default=None)
    password: str = Field(max_length=20)


# Modelo para criar tabelas
class User(UserBaseModel, table=True):
    # Type hint == attribute type, None == nullable

    # Valor padrão None/Null, caso contrário ainda será necessário passar o dado na instância
    # Gerado pelo database, não pela instância
    id_user: int | None = Field(default=None, primary_key=True)

    accounts: list['Account'] = Relationship(
        back_populates='user', passive_deletes='all'
    )


# Modelo com atributos necessários para criar um usuário
class UserCreateModel(UserBaseModel):
    pass


# Modelo com atributos para atualizar um usuário com Patch
class UserPatchUpdateModel(UserBaseModel):
    fullname: str | None = None
    username: str | None = None
    cpf: str | None = None
    password: str | None = None


# Modelo com os atributos obrigatórios que são retornados para o cliente
class UserPublicModel(SQLModel):
    id_user: int
    fullname: str
    username: str
    cpf: str
    address: str
    birth_date: str


# Modelo com a lista de contas
class UserPublicAccountsModel(UserPublicModel):
    accounts: list['AccountPublicModel'] | None = []
