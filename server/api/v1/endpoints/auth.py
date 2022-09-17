from typing import *

import jwt
from bcrypt import checkpw
from fastapi import APIRouter, Body, Header, HTTPException, Request, Cookie, Query
from fastapi.responses import JSONResponse, Response
from starlette import status as http_statuses

from data.models.user import LoginUserInput, RegisterUserInput
from data.repositories.user import User as UserRepository
from settings.settings import settings

router = APIRouter()


@router.post('/register')
def register_user(data: RegisterUserInput = Body(...)):
    if data.password != data.repeat_password:
        raise HTTPException(http_statuses.HTTP_400_BAD_REQUEST, detail='Passwords not match')
    repo = UserRepository()
    exists = repo.fetch(email=data.email) is not None
    if exists:
        raise HTTPException(http_statuses.HTTP_400_BAD_REQUEST, detail='User with the same Email address exists')
    user = repo.insert(info=data)
    return JSONResponse(user.serialize(exclude={'hashed_password'}), status_code=http_statuses.HTTP_201_CREATED)


@router.post('/login')
def login_user(authorization: Optional[str] = Header(None),
               data: Optional[LoginUserInput] = Body(None)):
    repo = UserRepository()
    user = None
    password_matched = True
    user_exists = False
    if authorization:
        authorization = authorization.replace('Bearer ', '')
        try:
            session_info = jwt.decode(authorization, settings.SECRET, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError as e:
            session_info = dict()
        email = session_info.get('sub', None)
        user = repo.fetch(email=email)
        user_exists = user is not None
    if data:
        user = repo.fetch(email=data.email)
        user_exists = user is not None
        if user_exists:
            password_matched = checkpw(password=data.password.encode('utf-8'),
                                       hashed_password=user.hashed_password.encode('utf-8'))
    if user_exists and password_matched:
        authorization = jwt.encode(payload={'sub': data.email}, key=settings.SECRET, algorithm='HS256')
        serialized_user = user.serialize(exclude={'hashed_password'}, by_alias=True)
        serialized_user.update({
            'token': authorization
        })
        response = JSONResponse(content={"user": serialized_user})
        return response
    else:
        response = JSONResponse(content={"error": 'Invalid email or password'},
                                status_code=http_statuses.HTTP_400_BAD_REQUEST)
        return response


@router.get('/logout')
def logout_user():
    response = Response(status_code=http_statuses.HTTP_204_NO_CONTENT)
    return response


@router.get('/getUser')
def get_user(authorization: Optional[str] = Header(None)):
    repo = UserRepository()
    serialized_user = None
    if authorization:
        authorization = authorization.replace('Bearer ', '')
        try:
            session_info = jwt.decode(authorization, key=settings.SECRET, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError as e:
            session_info = dict()
        email = session_info.get('sub', None)
        user = repo.fetch(email=email)
        if user:
            serialized_user = user.serialize(exclude={'hashed_password'}, by_alias=True)
            if authorization:
                serialized_user.update({
                    'token': authorization
                })
    return JSONResponse(content={"user": serialized_user},
                        status_code=http_statuses.HTTP_200_OK)
