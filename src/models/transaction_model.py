from decimal import Decimal
from enum import Enum

from sqlmodel import Column, Field, Relationship, SQLModel
from sqlmodel import Enum as sa_enum

from .account_model import Account


class TransactionType(Enum):
    saque = 'saque'
    deposito = 'depósito'


class TransactionBaseModel(SQLModel):
    # Se conta for deletada, remova todas as transações associadas. Apropriado para interações diretas com db, diferente de cascade_delete em Relationship no qual o código que é responsável pela remoção automática
    id_account: int | None = Field(
        default=None, foreign_key='account.id_account', ondelete='CASCADE'
    )
    transaction_type: TransactionType = Field(
        sa_column=Column(sa_enum(TransactionType), nullable=False)
    )
    transaction_value: Decimal = Field(decimal_places=2)


class Transaction(TransactionBaseModel, table=True):
    id_transaction: int | None = Field(default=None, primary_key=True)

    account: Account | None = Relationship(back_populates='transactions')


class TransactionCreateModel(TransactionBaseModel):
    pass


class TransactionPublicModel(TransactionBaseModel):
    id_transaction: int
