"""
    Moduł definiujący konektory do bazy danych.
"""

import sqlite3

from amelia.config import Config


class InvalidSqlQuery(Exception):
    """
        Wyjątek reprezentujący nieprawidłowo skonstruowane zapytanie SQL.
    """
    pass


class SqlQuery(str):
    """
        Obiekt reprezentujący generyczne zapytanie SQL.
        Wykonuje wstępną walidację treści zapytania.
    """
    SQL_STATEMENT = None

    def __init__(self, raw_query):
        if not raw_query.startswith(self.SQL_STATEMENT):
            raise InvalidSqlQuery('Invalid SQL query')


class InsertQuery(SqlQuery):
    SQL_STATEMENT = 'INSERT'


class UpdateQuery(SqlQuery):
    SQL_STATEMENT = 'UPDATE'


class DeleteQuery(SqlQuery):
    SQL_STATEMENT = 'DELETE'


class SelectQuery(SqlQuery):
    SQL_STATEMENT = 'SELECT'


class MultiSelectQuery(SelectQuery):
    pass


class WithDb(object):
    """
        Manadżer kontekstowy do obsługi połączenia z bazą danych sqlite3.
        Zwraca instancję WithDb jako obiekt konektora.
        Przy opuszczeniu bloku `with` następuje zatwierdzenie bądź wycofanie transakcji,
        w zależności od tego, czy wystąpił wyjątek.

        Kontektor wymaga obiektów typu SqlQuery do wykonywania zapytań.
        Ma to na celu wymuszenie świadomego tworzenia dedykowanych obiektów do zapytań SQL.
    """
    _connection = None
    _cursor = None

    def __init__(self):
        self._connection = sqlite3.connect(Config().app_db)
        self._cursor = self._connection.cursor()

    def _execute(self, sql_query, values=None):
        """
            Prywatna metoda bezpośrednio wykonująca zapytanie SQL.
        """
        if values:
            self._cursor.execute(sql_query, values)
        else:
            self._cursor.execute(sql_query)

    def insert(self, sql_query, values):
        """
            Wykonuje zapytanie zapisujące dane do BD (INSERT).
            sql_query powninen być spreparowanym zapytaniem SQL.
            Parametry należy przekazywać oddzielnie oraz za pomocą `?`.

            Zwraca id rekordu z klucza PK utworzonego rekordu.
        """
        if not isinstance(sql_query, InsertQuery):
            raise InvalidSqlQuery('InsertQuery object expected')
        self._execute(sql_query, values)
        return self._cursor.lastrowid

    def execute(self, sql_query, values):
        """
            Wykonuje operacje inne niż INSERT/SELECT.
        """
        if not isinstance(sql_query, (UpdateQuery, DeleteQuery)):
            raise InvalidSqlQuery('UpdateQuery or DeleteQuery object expected')
        self._execute(sql_query, values)

    def get_many(self, sql_query):
        """
            Odczytuje wiele rekordów z BD.
        """
        if not isinstance(sql_query, MultiSelectQuery):
            raise InvalidSqlQuery('MultiSelectQuery object expected')
        self._execute(sql_query)
        column_names = [name[0] for name in self._cursor.description]
        return (
            zip(column_names, values) for values in self._cursor.fetchall()
        )

    def __enter__(self):
        """
            Zwracja instancję WithDb - konektora do BD
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
            Zatwierdza albo wycofuje transakcję i zamyka połączenie z BD.
        """
        if exc_type:
            # w przypadku wystąpienia wyjątku, exec_type będzie różny od None
            self._connection.rollback()
            print('Transakcja wycofana.')
        else:
            self._connection.commit()
            print('Transakcja zatwierdzona.')
        self._connection.close()
