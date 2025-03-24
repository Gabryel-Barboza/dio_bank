from sqlmodel import Field, Relationship, SQLModel

from .account_model import Account


# TODO: enum type para transaction_type
class Transaction(SQLModel, table=True):
    id_transaction: int | None = Field(default=None, primary_key=True)
    # Se conta for deletada, remova todas as transações associadas. Apropriado para interações diretas com db
    id_account: int | None = Field(
        default=None, foreign_key='account.id_account', ondelete='CASCADE'
    )
    transaction_type: str
    transaction_value: float

    account: Account | None = Relationship(back_populates='transactions')
