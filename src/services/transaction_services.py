import functools
from decimal import Decimal
from uuid import UUID

from sqlmodel import Session, select

from src.models.account_model import Account
from src.models.transaction_model import Transaction
from src.utils.exceptions import (
    InsufficientBalanceException,
    InvalidOperationException,
    NonPositiveTransactionValueException,
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
    def create_transaction_log() -> Transaction:
        # Decoradores não podem ser corrotinas, são executados na avaliação de código fonte
        # Portanto, criar uma função síncrona wrapper para uma função assíncrona
        def wrapper(func):
            @functools.wraps(func)
            async def wrapped(*args, **kwargs):
                session: Session = kwargs['session']
                # Atualizar transação com o ID da conta recebido
                kwargs['transaction'].update({'id_account': kwargs['account_id']})

                await func(*args, **kwargs)
                # Objeto recebe a atualização no método
                transaction = kwargs['transaction']
                log = Transaction.model_validate(transaction)

                session.add(log)
                session.commit()

                return log

            return wrapped

        return wrapper

    @create_transaction_log()
    async def create_transaction(
        self, *, session: Session, transaction: dict, **kwargs
    ) -> None:
        account_id = transaction['id_account']
        account = session.get(Account, account_id)

        if not account:
            raise RegistryNotFoundException('Account not found!')

        transaction_type = transaction['transaction_type'].value
        transaction_value = transaction['transaction_value']

        if transaction_value <= 0:
            raise NonPositiveTransactionValueException

        # Atualizar transação com numeração de acordo com a conta
        # Por ser o mesmo objeto em referência no dicionário a alteração é refletida
        transaction.update({'transaction_no': len(account.transactions) + 1})

        match transaction_type:
            case 'saque':
                return await self._withdraw(session, account, transaction_value)
            case 'depósito':
                return await self._deposit(session, account, transaction_value)
            case _:
                raise InvalidOperationException

    @staticmethod
    async def read_transactions(
        session: Session,
        skip: int = 0,
        limit: int = 10,
        *,
        account_id: UUID = None,
        transaction_no: int = None,
    ) -> list[Transaction] | Transaction | None:
        if account_id:
            account = session.get(Account, account_id)

            if not account:
                raise RegistryNotFoundException('Account not found!')

            # ! Possui potencial para retornar uma grande quantidade de registros do banco
            transactions = account.transactions

            if transaction_no:
                try:
                    transaction = transactions[transaction_no - 1]
                except IndexError:
                    transaction = None

                if not transaction:
                    raise RegistryNotFoundException('Transaction not found!')

                return transaction

            return transactions

        else:
            transactions = session.exec(
                select(Transaction).offset(skip).limit(limit)
            ).all()

            return transactions
