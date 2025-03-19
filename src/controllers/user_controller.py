from fastapi import APIRouter

router = APIRouter(prefix='/users')

users = [{'name': 'Gabryel'}, {'name': 'Kaio'}]


@router.get('/')
async def get_users():
    return users


@router.get('/{id}')
async def get_user_by_id(id: int):
    return users[id]


@router.post('/')
async def create_user(user):
    users.append(user)


@router.patch('/')
async def update_user():
    pass


@router.delete('/')
async def delete_user(id: int):
    users.pop(id)
