import functools
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
    def create_transaction_log() -> None:
        # Decoradores não podem ser corrotinas, são executados na avaliação de código fonte
        # Portanto, criar uma função síncrona wrapper para uma função assíncrona
        def wrapper(func):
            @functools.wraps(func)
            async def wrapped(*args, **kwargs):
                # Atualizar transação com o ID da conta recebido
                kwargs['transaction'].update({'id_account': kwargs['id_account']})

                transaction = kwargs['transaction']
                session: Session = kwargs['session']
                log = Transaction.model_validate(transaction)

                session.add(log)
                await func(*args, **kwargs)
                session.commit()

            return wrapped

        return wrapper

    @create_transaction_log()
    async def create_transaction(
        self, *, session: Session, transaction: dict, **kwargs
    ) -> None:
        id_account = transaction['id_account']
        account = session.get(Account, id_account)

        if not account:
            raise RegistryNotFoundException

        transaction_type = transaction['transaction_type'].value
        transaction_value = transaction['transaction_value']

        match transaction_type:
            case 'saque':
                return await self._withdraw(session, account, transaction_value)
            case 'depósito':
                return await self._deposit(session, account, transaction_value)
            case _:
                raise InvalidOperationException

    @staticmethod
    async def read_transactions(
        session: Session, *, id_account: int = None, transaction_id: int = None
    ) -> list[Transaction] | Transaction | None:
        if transaction_id:
            transaction = session.get(Transaction, transaction_id)

            if not transaction:
                raise RegistryNotFoundException

            return transaction
        elif id_account:
            account = session.get(Account, id_account)

            if not account:
                raise RegistryNotFoundException

            return account.transactions

        else:
            accounts = session.exec(select(Transaction)).all()

            return accounts
