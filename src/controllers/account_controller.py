from fastapi import APIRouter, Depends, HTTPException, status

from src.databases.bank_db import Session, get_session
from src.models.account_model import (
    AccountCreateModel,
    AccountPatchUpdateModel,
    AccountPublicModel,
)
from src.models.transaction_model import TransactionPublicModel
from src.services.account_services import AccountServices
from src.services.transaction_services import TransactionServices
from src.utils.exceptions import (
    ExceedUserAccountsException,
    InsufficientBalanceException,
    InvalidOperationException,
    RegistryNotFoundException,
    UserNotFoundException,
)

acc_services = AccountServices()
transact_services = TransactionServices()

# TODO: Implementar campos de UUID (global) e ID (local)
router = APIRouter(prefix='/users', tags=['Account'])

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
    try:
        accounts = await acc_services.read_accounts(session, user_id=user_id)
    except RegistryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Account not found!'
        )
    else:
        return accounts


@router.get(
    '/accounts/{account_id}/',
    status_code=status.HTTP_200_OK,
)
async def get_account_by_id(
    *,
    session: Session = Depends(get_session),
    account_id: int,
) -> AccountPublicModel:
    try:
        account = await acc_services.read_accounts(session, account_id=account_id)
    except RegistryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Account not found!'
        )
    else:
        return account


@router.post(
    '/{user_id}/accounts/',
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    *,
    session: Session = Depends(get_session),
    account: AccountCreateModel,
    user_id: int,
) -> AccountPublicModel:
    try:
        account = await acc_services.insert_account(
            session, account.model_dump(), user_id
        )
    except UserNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.msg)
    except ExceedUserAccountsException as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.msg
        )
    else:
        return account


@router.put(
    '/accounts/{account_id}/',
    status_code=status.HTTP_201_CREATED,
)
async def update_account(
    *,
    session: Session = Depends(get_session),
    fields: AccountCreateModel,
    account_id: int,
) -> None:
    try:
        await acc_services.update_account(session, fields, account_id)
    except RegistryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Account not found!'
        )

    return


@router.patch(
    '/accounts/{account_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_account_fields(
    *,
    session: Session = Depends(get_session),
    fields: AccountPatchUpdateModel,
    account_id: int,
) -> None:
    try:
        await acc_services.update_account(
            session, fields.model_dump(exclude_unset=True), account_id
        )
    except RegistryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Account not found!'
        )

    return


@router.delete(
    '/accounts/{account_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_account(
    *,
    session: Session = Depends(get_session),
    account_id: int,
) -> None:
    try:
        await acc_services.delete_account(session, account_id)
    except RegistryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Account not found!'
        )

    return


# Transações


@router.get('/accounts/{account_id}/transactions/')
async def get_account_transactions(
    *,
    session: Session = Depends(get_session),
    account_id: int,
) -> list[TransactionPublicModel]:
    try:
        transactions = await transact_services.read_transactions(
            session, account_id=account_id
        )
    except RegistryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Account not found!'
        )
    else:
        return transactions


@router.get('/accounts/{account_id}/transactions/{transaction_id}')
async def get_account_transaction(
    *,
    session: Session = Depends(get_session),
    transaction_id: int,
) -> TransactionPublicModel:
    try:
        transaction = await transact_services.read_transactions(
            session, transaction_id=transaction_id
        )
    except RegistryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Transaction not found!'
        )
    else:
        return transaction


@router.post(
    '/accounts/{account_id}/transactions/',
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    *,
    session: Session,
):
    try:
        await transact_services.create_transaction()
    except (InvalidOperationException, InsufficientBalanceException) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.msg)
