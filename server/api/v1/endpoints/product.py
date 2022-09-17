from typing import *

import jwt
from fastapi import APIRouter, Query, Body, Path, Cookie, HTTPException, Request, Header
from data.models.product import CreateProductInfo, ProductInDB
from data.repositories.product import Product as ProductRepository
from data.repositories.user import User as UserRepository
from settings.settings import settings
from starlette import status as http_statuses

router = APIRouter()


@router.get('/')
def get_products(page: int = Query(1)):
    product_repo = ProductRepository()
    products = product_repo.all(offset=24 * (page - 1))
    products = list(map(lambda item: {**item, 'addedAt': item['created_at'].isoformat(), '_id': item['id']}, products))
    return {
        'products': products
    }


@router.get('/{category}')
def get_products_in_category(category: Optional[str] = Path(...), page: int = Query(1)):
    product_repo = ProductRepository()
    products = product_repo.all(category=category, offset=24 * (page - 1))
    products = list(map(lambda item: {**item, 'addedAt': item['created_at'].isoformat(), '_id': item['id']}, products))
    return {
        'products': products
    }


@router.post('/create')
def create_product(info: CreateProductInfo = Body(...),
                   authorization: Optional[str] = Header(None)):
    product_repo = ProductRepository()
    user_repo = UserRepository()
    if authorization:
        authorization = authorization.replace('Bearer ', '')
        try:
            session_info = jwt.decode(authorization, settings.SECRET, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError as e:
            session_info = dict()
        email = session_info.get('sub', None)
        user = user_repo.fetch(email=email)
    else:
        raise HTTPException(http_statuses.HTTP_401_UNAUTHORIZED)
    result = product_repo.insert(info=info, owner_email=user.email)
    if result:
        return {
            'productId': result.product_id,
        }
    return


@router.get('/specific/{id}')
def get_specific_product(product_id: int = Path(..., alias='id', title='id'),
                         authorization: Optional[str] = Header(None)):
    is_authenticated = False
    user_repo = UserRepository()
    logged_in_user_id = 0
    if authorization:
        authorization = authorization.replace('Bearer ', '')
        try:
            session_info = jwt.decode(authorization, settings.SECRET, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError as e:
            session_info = dict()
        email = session_info.get('sub', None)
        user = user_repo.fetch(email=email)
        logged_in_user_id = user.user_id
        is_authenticated = user is not None
    product_repo = ProductRepository()
    product = product_repo.fetch(product_id=product_id)
    if product:
        owner_user = user_repo.find_by_id(user_id=product['owner'])
        is_seller = owner_user.user_id == logged_in_user_id
        created_sells = product_repo.count_of_created_sells_by_user(owner_user.user_id)
        result = {
            '_id': product_id,
            'title': product['title'],
            'price': product['price'],
            'category': product['category_title'],
            'description': product['description'],
            'city': product['city_name'],
            'image': product['image'],
            'seller': product['owner'],
            'addedAt': product['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
            'isAuth': is_authenticated,
            'isSeller': is_seller,
            'isWished': False,
            'createdSells': created_sells
        }
        if is_authenticated:
            result.update({
                'email': owner_user.email,
                'name': owner_user.name,
                'phoneNumber': owner_user.phone_number,
                'avatar': owner_user.avatar
            })
        return result
    return


@router.patch('/edit/{id}')
def edit_product(info: ProductInDB = Body(...),
                 authorization: Optional[str] = Header(None)):
    product_repo = ProductRepository()
    user_repo = UserRepository()
    if authorization:
        authorization = authorization.replace('Bearer ', '')
        try:
            session_info = jwt.decode(authorization, settings.SECRET, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError as e:
            session_info = dict()
        email = session_info.get('sub', None)
        user = user_repo.fetch(email=email)
    else:
        raise HTTPException(http_statuses.HTTP_401_UNAUTHORIZED)
    result = product_repo.update(info=info, updater_user_id=user.user_id)
    # if result:
    return {
        'productId': info.product_id,
    }
    # raise HTTPException(status_code=http_statuses.HTTP_422_UNPROCESSABLE_ENTITY)
