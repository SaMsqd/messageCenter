from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from app.db import User, register_account, delete_account
from app.users import current_active_user
from app.schemas import AccountReceive


router = APIRouter()


@router.post('/register_account',
             description='Добавить новый аккаунт авито в БД')
async def account_db(account: AccountReceive, user: User = Depends(current_active_user)):
    try:
        await register_account(account, user)
        return Response(status_code=200, content={'detail': f'Аккаунт успешно добавлен в базу данных для юзера {user.id}'})
    except KeyError:
        raise HTTPException(status_code=432, detail='Ошибка при попытке получить токен доступа, возможно была допущена ошибка'
                                                    ' в данных аккаунта. Операция не выполнена')


@router.delete('/delete_account',
               description='Удаляет аккаунт из БД. Обязательно заполнить поле: profile_id')
async def delete_account_db(account: AccountReceive, user: User = Depends(current_active_user)):
    result = await delete_account(account, user)
    if not result:
        return Response(status_code=200, content=f'Аккаунт {account.profile_id} успешно удалён')
    raise HTTPException(status_code=result['status_code'], detail=result['detail'])
