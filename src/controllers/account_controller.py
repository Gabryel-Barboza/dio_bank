from fastapi import APIRouter

# TODO: Implementar rota adequada para especificar usuário
router = APIRouter(prefix='/users/{user_id}/accounts', tags=['Account'])


@router.get('/')
async def get_accounts(user_id: int):
    pass


@router.get('/{account_id}/')
async def get_account_by_id(user_id: int, account_id: int):
    pass


@router.post('/')
async def create_account(user_id: int):
    pass


@router.put('/{account_id}/')
async def update_account(user_id: int):
    pass


@router.patch('/{account_id}/')
async def update_account_fields(user_id: int):
    pass


@router.delete('/{account_id}/')
async def delete_account(user_id: int):
    pass


@router.get('/{account_id}/transactions/')
async def get_account_transactions(user_id: int, account_id: int):
    pass


@router.get('/{account_id}/transactions/{transaction_id}')
async def get_account_transaction(user_id: int, account_id: int, transaction_id: int):
    pass
