from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

# Resolve circular import, constante True apenas para IDEs. Com o interpretador direto é False
if TYPE_CHECKING:
    from .transaction_model import Transaction


# TODO: enum type para account_type
class Account(SQLModel, table=True):
    id_account: int | None = Field(default=None, primary_key=True)
    id_user: int | None = Field(default=None, foreign_key='user.id_user')
    balance: float = Field(default=0.0)
    account_type: str

    # Deleta transações associadas se a conta for deletada. 'Transaction' é um wrapper para type hint
    # É interpretado como uma string, mas a IDE identifica como tipo.
    # Se retirasse as aspas, ocasionaria em erro do interpretador devido ao import
    transactions: list['Transaction'] = Relationship(
        back_populates='account', cascade_delete=True, passive_deletes='all'
    )
    # passive_deletes desativa tratamento padrão do SQLAlchemy, onde o campo associado é setado como nulo antes do atributo ser deletado, inutilizando restrições como ondelete= e outros.
