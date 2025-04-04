from sqlmodel import Session, select

from src.models.account_model import Account
from src.models.user_model import User
from src.utils.exceptions import (
    ExceedUserAccountsException,
    RegistryNotFoundException,
    UserNotFoundException,
)


class AccountServices:
    MAX_ACCOUNTS = 3

    @staticmethod
    async def read_accounts(
        session: Session, *, user_id: int = None, id_account: int = None
    ) -> list[Account] | Account | None:
        if id_account:  # Recuperar única conta
            account = session.get(Account, id_account)

            if not account:
                raise RegistryNotFoundException('Account not found!')

            return account
        elif user_id:  # Recuperar contas de único usuário
            user = session.get(User, user_id)

            if not user:
                raise RegistryNotFoundException('User not found!')

            return user.accounts
        else:  # Recuperar todas as contas
            accounts = session.exec(select(Account)).all()

            return accounts

    async def insert_account(
        self, session: Session, account: dict, user_id: int
    ) -> Account:
        user = session.get(User, user_id)

        if not user:
            raise UserNotFoundException

        if len(user.accounts) >= self.MAX_ACCOUNTS:
            raise ExceedUserAccountsException(self.MAX_ACCOUNTS)

        account.update({'id_user': user_id})
        account = Account.model_validate(account)

        session.add(account)
        session.commit()
        session.refresh(account)

        return account

    @staticmethod
    async def update_account(session: Session, fields: dict, id_account: int) -> None:
        account = session.get(Account, id_account)

        if not account:
            raise RegistryNotFoundException('Account not found!')

        account.sqlmodel_update(fields)

        session.add(account)
        session.commit()

        return

    @staticmethod
    async def delete_account(session: Session, id_account: int) -> None:
        account = session.get(Account, id_account)

        if not account:
            raise RegistryNotFoundException('Account not found!')

        session.delete(account)
        session.commit()

        return
