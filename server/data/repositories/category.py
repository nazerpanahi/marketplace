from data.models.category import Category as CategoryModel, CategoryInDB
from data.connections.postgres import Postgres


class Category(Postgres):
    def __init__(self):
        pass

    def insert(self, info: CategoryModel):
        insert_category_query = f"""
        INSERT INTO shop.categories
        (title, description)
        VALUES (
            %(title)s, %(description)s
        )
        RETURNING id
        """
        transaction = self.transaction()
        transaction.begin()
        try:
            transaction.execute(query=insert_category_query, params={**info.dict(by_alias=True)})
            query_result = transaction.fetchone()
            category_id = query_result['id']
            result = CategoryInDB(id=category_id, **info.dict(by_alias=True))
        except Exception as e:
            result = None
            transaction.rollback()
        finally:
            transaction.end()
        return result

    def fetch(self, category_id: int):
        raise NotImplementedError

    def all(self):
        query = f"""
        SELECT c.* FROM shop.categories as c
        """
        query_result = self.select(query)
        if len(query_result) > 0:
            return list(map(lambda item: CategoryInDB(**item), query_result))
        return None
