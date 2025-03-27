from decimal import Decimal

from sqlmodel import Session, select

from src.models.account_model import Account
from src.models.transaction_model import Transaction
from src.utils.exceptions import (
    InsufficientBalanceException,
    InvalidOperationException,
    RegistryNotFoundException,
)


class TransactionServices:
    # Operação de saque
    @staticmethod
    async def _withdraw(session: Session, account: Account, withdraw_amount: Decimal):
        if account.balance < withdraw_amount:
            raise InsufficientBalanceException

        account.balance -= withdraw_amount
        session.add(account)

    # Operação de depósito
    @staticmethod
    async def _deposit(session: Session, account: Account, deposit_amount: Decimal):
        account.balance += deposit_amount
        session.add(account)

    @staticmethod
    def create_transaction_log(func, session: Session, *args, **kwargs) -> None:
        log: Transaction = kwargs['transaction']
        session.add(log)
        func(*args, **kwargs)
        session.commit()

    @create_transaction_log
    async def create_transaction(
        self, session: Session, account_id: int, transaction_type: int, *args, **kwargs
    ) -> None:
        account = session.get(Account, account_id)

        match transaction_type:
            case 1:
                return self._withdraw(session, account, *args, **kwargs)
            case 2:
                return self._deposit(session, account, *args, **kwargs)
            case _:
                raise InvalidOperationException

    @staticmethod
    async def read_transactions(
        session: Session, *, account_id: int = None, transaction_id: int = None
    ) -> list[Transaction] | Transaction | None:
        if transaction_id:
            transaction = session.get(Transaction, transaction_id)

            if not transaction:
                raise RegistryNotFoundException

            return transaction
        elif account_id:
            account = session.get(Account, account_id)

            if not account:
                raise RegistryNotFoundException

            return account.transactions

        else:
            accounts = session.exec(select(Transaction)).all()

            return accounts
