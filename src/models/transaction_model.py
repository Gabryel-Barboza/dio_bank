from decimal import Decimal

from sqlmodel import Field, Relationship, SQLModel

from .account_model import Account


class TransactionBaseModel(SQLModel):
    # Se conta for deletada, remova todas as transações associadas. Apropriado para interações diretas com db, diferente de cascade_delete em Relationship no qual o código que é responsável pela remoção automática
    id_account: int | None = Field(
        default=None, foreign_key='account.id_account', ondelete='CASCADE'
    )
    transaction_type: str
    transaction_value: Decimal


class Transaction(TransactionBaseModel, table=True):
    id_transaction: int | None = Field(default=None, primary_key=True)

    account: Account | None = Relationship(back_populates='transactions')


class TransactionPublicModel(TransactionBaseModel):
    id_transaction: int
