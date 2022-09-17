from data.models.user import UserInDatabase, RegisterUserInput
from bcrypt import hashpw, gensalt
from data.connections.postgres import Postgres


class User(Postgres):
    def __init__(self):
        pass

    def insert(self, info: RegisterUserInput):
        query = f"""
        INSERT INTO shop.users 
        (email, name, last_name, phone_number, gender, hashed_password, created_at, updated_at, deleted_at)
        VALUES (
            %(email)s, %(name)s, %(last_name)s, 
            %(phone_number)s, %(gender)s, %(hashed_password)s, 
            %(created_at)s, %(updated_at)s, %(deleted_at)s
        )
        RETURNING id
        """
        hashed_password = hashpw(info.password.encode('utf-8'), salt=gensalt()).decode('utf-8')
        database_info = UserInDatabase(**info.dict(by_alias=True), hashed_password=hashed_password)
        transaction = self.transaction()
        transaction.begin()
        try:
            transaction.execute(query=query, params=database_info.dict())
            transaction.fetchone()
        finally:
            transaction.end()
        return database_info

    def fetch(self, email: str):
        query = f"""
        SELECT * from shop.users as u
        WHERE u.email = %(email)s
        """
        result = self.select(query, {'email': email})
        if len(result) > 0:
            result = dict(result[0].items())
            result = UserInDatabase(
                id=result['id'],
                email=result['email'],
                name=result['name'],
                lastName=result['last_name'],
                phoneNumber=result['phone_number'],
                gender=result['gender'],
                hashed_password=result['hashed_password'],
                created_at=result['created_at'],
                updated_at=result['updated_at'],
                deleted_at=result['deleted_at'],
            )
        else:
            result = None
        return result

    def find_by_id(self, user_id: int):
        query = f"""
        SELECT * from shop.users as u
        WHERE u.id = %(id)s
        """
        result = self.select(query, {'id': str(user_id)})
        if len(result) > 0:
            result = dict(result[0].items())
            result = UserInDatabase(
                id=result['id'],
                email=result['email'],
                name=result['name'],
                lastName=result['last_name'],
                phoneNumber=result['phone_number'],
                gender=result['gender'],
                hashed_password=result['hashed_password'],
                created_at=result['created_at'],
                updated_at=result['updated_at'],
                deleted_at=result['deleted_at'],
            )
        else:
            result = None
        return result
