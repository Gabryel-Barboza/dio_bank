from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Column, Field, Relationship, SQLModel
from sqlmodel import Enum as sa_enum

# Resolve circular import, constante True apenas para IDEs. Com o interpretador Python direto é False
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
    balance: Decimal = Field(default=Decimal(), decimal_places=2)


class Account(AccountBaseModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    account_no: int = Field(nullable=False)
    id_user: UUID | None = Field(
        default=None, foreign_key='user.id', ondelete='CASCADE'
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


class AccountPublicModel(AccountBaseModel):
    account_no: int
    id_user: UUID
    id: UUID
