from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import PositiveInt

from src.controllers.auth_controller import get_user_authentication
from src.databases.bank_db import Session, get_session
from src.models.account_model import (
    AccountCreateModel,
    AccountPublicModel,
)
from src.models.transaction_model import TransactionCreateModel, TransactionPublicModel
from src.services.account_services import AccountServices
from src.services.transaction_services import TransactionServices

acc_services = AccountServices()
transact_services = TransactionServices()

router = APIRouter(
    prefix='/users', tags=['Account'], dependencies=[Depends(get_user_authentication)]
)


# Contas
@router.get(
    '/accounts/',
    status_code=status.HTTP_200_OK,
)
async def get_accounts(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = Query(default=10, le=10),
) -> list[AccountPublicModel] | None:
    accounts = await acc_services.read_accounts(session, skip, limit)

    return accounts


@router.get(
    '/{user_id}/accounts/',
    status_code=status.HTTP_200_OK,
)
async def get_user_accounts(
    *,
    session: Session = Depends(get_session),
    user_id: UUID,
) -> list[AccountPublicModel]:
    accounts = await acc_services.read_accounts(session, user_id=user_id)

    return accounts


@router.get(
    '/accounts/{account_id}/',
    status_code=status.HTTP_200_OK,
)
async def get_account_by_id(
    *,
    session: Session = Depends(get_session),
    account_id: UUID,
) -> AccountPublicModel:
    account = await acc_services.read_accounts(session, account_id=account_id)

    return account


@router.post(
    '/{user_id}/accounts/',
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    *,
    session: Session = Depends(get_session),
    account: AccountCreateModel = {},
    user_id: UUID,
) -> AccountPublicModel:
    account = await acc_services.insert_account(session, account.model_dump(), user_id)

    return account


@router.delete(
    '/accounts/{account_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_account(
    *,
    session: Session = Depends(get_session),
    account_id: UUID,
) -> None:
    await acc_services.delete_account(session, account_id)

    return


# Transações
@router.get(
    '/accounts/{account_id}/transactions/',
    status_code=status.HTTP_200_OK,
)
async def get_account_transactions(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = Query(default=50, le=50),
    account_id: UUID,
) -> list[TransactionPublicModel]:
    transactions = await transact_services.read_transactions(
        session, skip, limit, account_id=account_id
    )

    return transactions


@router.get(
    '/accounts/{account_id}/transactions/{transaction_no}',
    status_code=status.HTTP_200_OK,
)
async def get_account_transaction(
    *,
    session: Session = Depends(get_session),
    account_id: UUID,
    transaction_no: PositiveInt,
) -> TransactionPublicModel | None:
    transaction = await transact_services.read_transactions(
        session, account_id=account_id, transaction_no=transaction_no
    )

    return transaction


@router.post(
    '/accounts/{account_id}/transactions/',
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    *,
    session: Session = Depends(get_session),
    account_id: UUID,
    transaction: TransactionCreateModel,
    transaction_args: dict = {},
) -> TransactionPublicModel:
    transaction = await transact_services.create_transaction(
        session=session,
        account_id=account_id,
        transaction=transaction.model_dump(),
        transaction_args=transaction_args,
    )

    return transaction
