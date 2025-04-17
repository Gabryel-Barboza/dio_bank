from uuid import UUID

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
        session: Session,
        skip: int = 0,
        limit: int = 10,
        *,
        user_id: UUID = None,
        account_id: UUID = None,
    ) -> list[Account] | Account | None:
        if account_id:  # Recuperar única conta
            account = session.get(Account, account_id)

            if not account:
                raise RegistryNotFoundException('Account not found!')

            return account
        elif user_id:  # Recuperar contas de único usuário
            user = session.get(User, user_id)

            if not user:
                raise RegistryNotFoundException('User not found!')

            return user.accounts
        else:  # Recuperar todas as contas
            accounts = session.exec(select(Account).offset(skip).limit(limit)).all()

            return accounts

    async def insert_account(
        self, session: Session, account: dict, user_id: UUID
    ) -> Account:
        user = session.get(User, user_id)

        if not user:
            raise UserNotFoundException

        total_user_accounts = len(user.accounts)

        if total_user_accounts >= self.MAX_ACCOUNTS:
            raise ExceedUserAccountsException(self.MAX_ACCOUNTS)

        account.update({'id_user': user_id, 'account_no': total_user_accounts + 1})
        account = Account.model_validate(account)

        session.add(account)
        session.commit()
        session.refresh(account)

        return account

    @staticmethod
    async def delete_account(session: Session, account_id: UUID) -> None:
        account = session.get(Account, account_id)

        if not account:
            raise RegistryNotFoundException('Account not found!')

        session.delete(account)
        session.commit()

        return
