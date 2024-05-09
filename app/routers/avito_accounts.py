import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from app.database.methods import account_methods as db
from app.database.db import User
from app.users import current_active_user
from app.schemas import AccountReceive

from sqlalchemy.exc import IntegrityError


router = APIRouter()


@router.post('/register_account',
             description='Добавить новый аккаунт авито в БД')
async def register_account(account: AccountReceive, user: User = Depends(current_active_user)):
    try:
        account_handler = await db.account_receive_to_handler(account)
        account_handler.api.register_webhook(os.getenv('URL')+'/webhook/'+str(user.id)+'/accept')
        await db.register_account(account, user)
        return Response(status_code=200, content={'detail': f'Аккаунт успешно добавлен в базу данных для юзера '
                                                            f'{user.id}. Webhook зарегистрирован успешно'})

    except KeyError:
        raise HTTPException(status_code=432, detail='Ошибка при попытке получить токен доступа, возможно была допущена ошибка'
                                                    ' в данных аккаунта. Операция не выполнена')
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Аккаунт уже существует')


@router.delete('/delete_account',
               description='Удаляет аккаунт из БД. Обязательно заполнить поле: profile_id')
async def delete_account(account: AccountReceive, user: User = Depends(current_active_user)):
    result = await db.delete_account(account, user)
    if not result:
        return Response(status_code=200, content=f'Аккаунт {account.profile_id} успешно удалён')

    raise HTTPException(status_code=result['status_code'], detail=result['detail'])


@router.get('/get_accounts', description='Возвращает список аккаунтов авито')
async def get_accounts(user: User = Depends(current_active_user)):
    return await db.get_accounts(user)
