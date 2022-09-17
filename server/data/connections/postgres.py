import psycopg2
from psycopg2 import extras as e
import threading
from typing import *

from settings.settings import settings
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_fixed


class PostgresLockException(Exception):
    pass


class PostgresTransaction:
    def __init__(self, connection: e.RealDictConnection, lock_timeout_seconds: float = -1):
        self._connection: e.RealDictConnection = connection
        self._cursor: Union[e.RealDictCursor, type(None)] = None
        self._lock = threading.Lock()
        self._lock_timeout_seconds = lock_timeout_seconds

    @retry(retry=retry_if_exception(lambda ex: isinstance(ex, PostgresLockException)),
           stop=stop_after_attempt(3),
           wait=wait_fixed(0.1))
    def begin(self):
        self.acquire()
        try:
            if not self._cursor or self._cursor:
                self._cursor = self._connection.cursor()
        finally:
            self.release()

    def end(self, close_connection: bool = True):
        self.commit()
        self.close_transaction()
        if close_connection:
            self.close_connection()

    def execute(self, query: str, params: Union[List[str], Dict[str, str]] = None):
        self._cursor.execute(query, params)

    def execute_values(self,
                       query: str,
                       values: List[Union[List[str], Dict[str, str]]],
                       page_size=100,
                       fetch: bool = False):
        e.execute_values(self._cursor, query, values, page_size=page_size, fetch=fetch)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchmany(self, size: int = None):
        return self._cursor.fetchmany(size)

    def fetchall(self):
        return self._cursor.fetchall()

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def close_connection(self):
        self._connection.close()

    def close_transaction(self):
        self._cursor.close()

    def acquire(self, timeout: float = None):
        if not timeout:
            timeout = self._lock_timeout_seconds
        acquired = self._lock.acquire(timeout=timeout)
        if not acquired:
            raise PostgresLockException('cannot acquire transaction lock')

    def release(self):
        self._lock.release()


class Postgres:
    _connections = dict()
    _lock = threading.Lock()
    _lock_timeout_second = 0.1

    @classmethod
    def __get_new_connection(cls) -> e.RealDictConnection:
        return psycopg2.connect(
            host=settings.PG_HOST,
            port=settings.PG_PORT,
            database=settings.PG_DATABASE,
            user=settings.PG_USER,
            password=settings.PG_PASSWORD,
            cursor_factory=e.RealDictCursor,
            connection_factory=e.RealDictConnection,
            application_name=settings.APP_TITLE,
        )

    @classmethod
    @retry(retry=retry_if_exception(lambda ex: isinstance(ex, PostgresLockException)),
           stop=stop_after_attempt(3),
           wait=wait_fixed(0.1))
    def __get_connection(cls, name: str = None):
        name = name or settings.APP_TITLE
        acquired = cls._lock.acquire(timeout=cls._lock_timeout_second)
        if not acquired:
            raise PostgresLockException('cannot acquire connection lock')
        if name not in cls._connections or cls._connections[name].closed:
            cls._connections[name] = cls.__get_new_connection()
            cls._connections[name].autocommit = True
        cls._lock.release()
        return cls._connections[name]

    @classmethod
    def select(cls,
               query: str,
               params: Union[List[str], Dict[str, str]] = None) -> List[e.RealDictRow]:
        connection = cls.__get_connection()
        cursor: e.RealDictCursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        connection.commit()
        return result

    @classmethod
    def execute(cls, query: str, params: Union[List[str], Dict[str, str]] = None, fetch_result: bool = False):
        connection = cls.__get_connection()
        cursor: e.RealDictCursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()

        result = None
        if fetch_result:
            result = cursor.fetchone()
        return result

    @classmethod
    def transaction(cls):
        return PostgresTransaction(connection=cls.__get_new_connection(),
                                   lock_timeout_seconds=cls._lock_timeout_second)
