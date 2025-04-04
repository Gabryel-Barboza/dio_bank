from fastapi import APIRouter, Depends, status

from src.controllers.auth_controller import get_user_authentication
from src.databases.bank_db import Session, get_session
from src.models.account_model import (
    AccountCreateModel,
    AccountPatchUpdateModel,
    AccountPublicModel,
)
from src.models.transaction_model import TransactionCreateModel, TransactionPublicModel
from src.services.account_services import AccountServices
from src.services.transaction_services import TransactionServices

acc_services = AccountServices()
transact_services = TransactionServices()

# TODO: Implementar campos de UUID (global) e ID (local)
# TODO: Impedir valores negativos para saldo da conta
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
) -> list[AccountPublicModel] | None:
    accounts = await acc_services.read_accounts(session)

    return accounts


@router.get(
    '/{user_id}/accounts/',
    status_code=status.HTTP_200_OK,
)
async def get_user_accounts(
    *,
    session: Session = Depends(get_session),
    user_id: int,
) -> list[AccountPublicModel]:
    accounts = await acc_services.read_accounts(session, user_id=user_id)

    return accounts


@router.get(
    '/accounts/{id_account}/',
    status_code=status.HTTP_200_OK,
)
async def get_account_by_id(
    *,
    session: Session = Depends(get_session),
    id_account: int,
) -> AccountPublicModel:
    account = await acc_services.read_accounts(session, id_account=id_account)

    return account


@router.post(
    '/{user_id}/accounts/',
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    *,
    session: Session = Depends(get_session),
    account: AccountCreateModel = {},
    user_id: int,
) -> AccountPublicModel:
    account = await acc_services.insert_account(session, account.model_dump(), user_id)

    return account


@router.put(
    '/accounts/{id_account}/',
    status_code=status.HTTP_201_CREATED,
)
async def update_account(
    *,
    session: Session = Depends(get_session),
    fields: AccountCreateModel,
    id_account: int,
) -> None:
    await acc_services.update_account(session, fields, id_account)

    return


@router.patch(
    '/accounts/{id_account}/',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_account_fields(
    *,
    session: Session = Depends(get_session),
    fields: AccountPatchUpdateModel,
    id_account: int,
) -> None:
    await acc_services.update_account(
        session, fields.model_dump(exclude_unset=True), id_account
    )

    return


@router.delete(
    '/accounts/{id_account}/',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_account(
    *,
    session: Session = Depends(get_session),
    id_account: int,
) -> None:
    await acc_services.delete_account(session, id_account)

    return


# Transações
@router.get(
    '/accounts/{id_account}/transactions/',
    status_code=status.HTTP_200_OK,
)
async def get_account_transactions(
    *,
    session: Session = Depends(get_session),
    id_account: int,
) -> list[TransactionPublicModel]:
    transactions = await transact_services.read_transactions(
        session, id_account=id_account
    )

    return transactions


@router.get(
    '/accounts/{id_account}/transactions/{transaction_id}',
    status_code=status.HTTP_200_OK,
)
async def get_account_transaction(
    *,
    session: Session = Depends(get_session),
    transaction_id: int,
) -> TransactionPublicModel:
    transaction = await transact_services.read_transactions(
        session, transaction_id=transaction_id
    )

    return transaction


@router.post(
    '/accounts/{id_account}/transactions/',
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    *,
    session: Session = Depends(get_session),
    id_account: int,
    transaction: TransactionCreateModel,
    transaction_args: dict = {},
):
    await transact_services.create_transaction(
        session=session,
        id_account=id_account,
        transaction=transaction.model_dump(),
        transaction_args=transaction_args,
    )

    return
