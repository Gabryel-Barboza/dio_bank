from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Column, Field, Relationship, SQLModel
from sqlmodel import Enum as sa_enum

# Resolve circular import, constante True apenas para IDEs. Com o interpretador direto é False
if TYPE_CHECKING:
    from .transaction_model import Transaction
    from .user_model import User


class AccountType(Enum):
    corrente = 'corrente'
    poupanca = 'poupança'


class AccountBaseModel(SQLModel):
    account_type: AccountType | None = Field(
        default=AccountType.corrente,
        sa_column=Column(sa_enum(AccountType), nullable=False),
    )
    balance: Decimal = Field(default=Decimal(0), decimal_places=2)


class Account(AccountBaseModel, table=True):
    id_account: int | None = Field(default=None, primary_key=True)
    id_user: int | None = Field(
        default=None, foreign_key='user.id_user', ondelete='CASCADE'
    )

    user: 'User' = Relationship(back_populates='accounts')
    # 'Transaction' é um wrapper para type hint
    # É interpretado como uma string, mas a IDE identifica como tipo.
    # Se retirasse as aspas, ocasionaria em erro do interpretador devido ao import
    transactions: list['Transaction'] = Relationship(
        back_populates='account', passive_deletes='all'
    )
    # passive_deletes desativa tratamento padrão do SQLAlchemy, onde o campo associado é setado como nulo antes do atributo ser deletado, inutilizando restrições como ondelete= e outros.


class AccountCreateModel(AccountBaseModel):
    pass


class AccountPatchUpdateModel(SQLModel):
    id_user: int | None = None
    account_type: str | None = None
    balance: Decimal | None = None


class AccountPublicModel(AccountBaseModel):
    id_account: int
    id_user: int
