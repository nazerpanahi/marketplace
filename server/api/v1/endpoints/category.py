from fastapi import APIRouter

from data.repositories.category import Category as CategoryRepository

router = APIRouter()


@router.get('/')
def get_categories():
    return {"categories": CategoryRepository().all()}
