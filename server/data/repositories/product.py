from data.models.product import CreateProductInfo, ProductInDB
from data.connections.postgres import Postgres


class Product(Postgres):
    def __init__(self):
        pass

    def insert(self, info: CreateProductInfo, owner_email: str):
        insert_product_query = f"""
        INSERT INTO shop.products
        (title, price, description, city, image, owner, category, is_active)
        VALUES (
            %(title)s, %(price)s, %(description)s, 
            (SELECT id as city FROM shop.cities WHERE city=%(city)s),
            %(image)s, 
            (SELECT id as owner FROM shop.users WHERE email=%(owner_email)s),
            (SELECT id FROM shop.categories WHERE title=%(category)s),
            %(is_active)s
        )
        RETURNING id
        """
        transaction = self.transaction()
        transaction.begin()
        try:
            transaction.execute(query=insert_product_query, params={**info.dict(by_alias=True),
                                                                    'is_active': True,
                                                                    'owner_email': owner_email})
            query_result = transaction.fetchone()
            product_id = query_result['id']
            result = ProductInDB(id=product_id, **info.dict(by_alias=True))
        except Exception as e:
            result = None
            transaction.rollback()
        finally:
            transaction.end()
        return result

    def fetch(self, product_id: int):
        query = f"""
        SELECT p.*, c.city as city_name, ctg.title as category_title FROM shop.products as p
        JOIN shop.cities as c ON c.id = p.city
        JOIN shop.categories as ctg ON ctg.id = p.category
        WHERE p.id = %(product_id)s
        """
        result = self.select(query, {'product_id': str(product_id)})
        if len(result) > 0:
            result = dict(result[0].items())
        else:
            result = None
        return result

    def count_of_created_sells_by_user(self, user_id: int):
        query = f"""
        SELECT count(*) as created_sells FROM shop.products as p
        WHERE p.owner = %(owner)s
        """
        result = self.select(query, {'owner': str(user_id)})
        return result[0]['created_sells']

    def all(self, category: str = None, limit: int = 24, offset: int = 0):
        if category:
            query = f"""
            SELECT p.*, ctg.title as category_title FROM shop.products as p
            JOIN shop.categories as ctg ON ctg.id = p.category
            WHERE ctg.title = %(category)s
            LIMIT {limit}
            OFFSET {offset}
            """
        else:
            query = f"""
            SELECT p.* FROM shop.products as p
            LIMIT {limit}
            OFFSET {offset}
            """
        result = self.select(query, {'category': category})
        return result

    def update(self, info: ProductInDB, updater_user_id: int):
        query = """
        UPDATE shop.products
        SET title = %(title)s, 
            price = %(price)s, 
            description = %(description)s, 
            city = (SELECT id as city FROM shop.cities WHERE city=%(city)s), 
            image = %(image)s,
            category = (SELECT id FROM shop.categories WHERE title=%(category)s), 
            is_active = %(is_active)s
        WHERE id = %(id)s and owner = %(user_id)s
        """

        result = self.execute(query, {'title': info.title,
                                      'price': info.price,
                                      'description': info.description,
                                      'city': info.city,
                                      'image': info.image,
                                      'category': info.category,
                                      'is_active': True,
                                      'id': info.product_id,
                                      'user_id': updater_user_id})
        return result
