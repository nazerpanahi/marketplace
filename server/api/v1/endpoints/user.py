from typing import *

import jwt
from fastapi import APIRouter, Header, Query
from fastapi.responses import JSONResponse
from starlette import status as http_statuses

from data.repositories.product import Product as ProductRepository
from data.repositories.user import User as UserRepository
from settings.settings import settings

router = APIRouter()


@router.get('/getUserById/{user_id}')
def get_user(user_id: int = Query(...), authorization: Optional[str] = Header(None)):
    user_repo = UserRepository()
    product_repo = ProductRepository()
    user = None
    serialized_user = None
    is_me = False
    if authorization:
        authorization = authorization.replace('Bearer ', '')
        try:
            session_info = jwt.decode(authorization, key=settings.SECRET, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError as e:
            session_info = dict()
        email = session_info.get('sub', None)
        logged_in_user = user_repo.fetch(email=email)
        user = logged_in_user
        if logged_in_user:
            is_me = logged_in_user.user_id == user_id
    if not is_me:
        user = user_repo.find_by_id(user_id=user_id)
    if user:
        serialized_user = user.serialize(exclude={'hashed_password'}, by_alias=True)
        created_sells = product_repo.count_of_created_sells_by_user(user_id=user_id)
        serialized_user.update({
            'isMe': is_me,
            'totalSells': created_sells,
        })
    return JSONResponse(content={"user": serialized_user},
                        status_code=http_statuses.HTTP_200_OK)
