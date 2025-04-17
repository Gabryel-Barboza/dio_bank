from datetime import date
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from .account_model import Account, AccountPublicModel


# Modelo base, se comporta como uma interface
class UserBaseModel(SQLModel):
    # Tipo TEXT para SQLite e VARCHAR(255) para MySQL, apenas VARCHAR para outros
    fullname: str
    username: str = Field(index=True, max_length=50, unique=True)
    address: str | None = Field(default=None)
    cpf: str = Field(index=True, min_length=11, max_length=11, unique=True)
    birth_date: date | None = Field(default=None)
    password: str = Field(max_length=20)


# Modelo para criar tabelas
class User(UserBaseModel, table=True):
    # Type hint == attribute type, None == nullable

    # Gerado pelo database, não pela instância, None e valor padrão para ser opcional na requisição
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    # Após hash a senha possui tamanho maior, portanto o limite padrão é atribuído
    password: str = Field()

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


# Modelo com os atributos obrigatórios que são retornados para o cliente, define a ordem dos atributos
class UserPublicModel(SQLModel):
    fullname: str
    username: str
    cpf: str
    address: str | None
    birth_date: date | None
    id: UUID


# Modelo com a lista de contas, evita recursão com Pydantic
class UserPublicAccountsModel(UserPublicModel):
    accounts: list[AccountPublicModel] | None = []


# Modelo para autenticação de usuário
class AccessToken(SQLModel):
    access_token: str
    token_type: str
