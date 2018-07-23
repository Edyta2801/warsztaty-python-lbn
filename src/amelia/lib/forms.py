# -*- coding: utf-8 -*-

"""
    Biblioteka z prototypami dla formularzy.
"""


from copy import deepcopy
from amelia.lib.db import (
    WithDb,
    InsertQuery,
    UpdateQuery,
    DeleteQuery,
    MultiSelectQuery,
    SelectQuery,

)


class InvalidDbOperation(Exception):
    """
        Klasa wyjątku do obsługi niedozwolonych operacji na bazie danych.
    """
    pass


class FieldNotFound(Exception):
    """
        Wyjątek do obsługi przypadku, gdy pole nie zostanie odnalezione w formularzu.
    """
    pass


class BaseDbModel(object):
    """
        Bazowy model danych implementujący API do operacji na bazie danych.
    """
    _id = None  # id rekordu w bazie danych
    _SQL_TABLENAME = None  # nazwa tabeli w bazie danych
    _SQL_INSERT = InsertQuery('INSERT INTO {table_name} ({columns}) VALUES ({values})')
    _SQL_UPDATE = UpdateQuery('UPDATE {table_name} SET {columns_values} WHERE id=?')
    _SQL_DELETE = DeleteQuery('DELETE FROM {table_name} WHERE id=?')
    _SQL_FETCH_ONE = SelectQuery('SELECT * FROM {table_name} WHERE id=?')
    _SQL_FETCH_MANY = MultiSelectQuery('SELECT * FROM {table_name}')

    def delete(self):
        """
            Destruktor obiektu - usuwa rekord z bazy danych.
        """
        if not self._id:
            raise InvalidDbOperation('id is required to perform SQL update query')
        with WithDb() as db:
            db.execute(
                DeleteQuery(self._SQL_DELETE.format(table_name=self._SQL_TABLENAME)), (self._id,)
            )

    def _db_values(self):
        """
            Zwraca krotki reprezentujące nazwy kolumn i wartości odczytane z pól formularza.
        """
        columns = []
        values = []
        for field in self.fields:
            columns.append("'{0}'".format(field.name))
            values.append(field.get_db_value())
        return columns, values

    def _save_data(self):
        """
            Zapisuje jeden (nowy) rekord w bazie danych
        """
        if self._id:
            # zabezpieczenie przez klonowaniem rekordu
            raise InvalidDbOperation('Record already exists with this id')
        columns, values = self._db_values()
        insert_query = self._SQL_INSERT.format(
            table_name=self._SQL_TABLENAME,
            columns=', '.join(columns),
            values=', '.join('?' * len(columns))
        )
        with WithDb() as db:
            self._id = db.insert(InsertQuery(insert_query), values)

    def _update_data(self):
        """
            Aktualizuje jeden rekord w bazie danych.
        """
        if not self._id:
            raise InvalidDbOperation('id is required to perform SQL update query')
        columns, values = self._db_values()
        columns_values = ["{0}=?".format(name) for name in columns]
        update_query = self._SQL_UPDATE.format(
            table_name=self._SQL_TABLENAME,
            columns_values=', '.join(columns_values)
        )
        with WithDb() as db:
            db.execute(UpdateQuery(update_query), values + [self._id])

    def load_one(self):
        """
            Wczytuje jeden rekord z bazy danych.
        """
        raise NotImplementedError

    @classmethod
    def all(cls):
        """
            Zwraca surową (niesformatowaną) listę rekordów.
        """
        with WithDb() as db:
            data_rows = db.get_many(
                MultiSelectQuery(cls._SQL_FETCH_MANY.format(table_name=cls._SQL_TABLENAME))
            )
        return data_rows

    @classmethod
    def load_many(cls):
        """
            Wczytuje wiele rekordów.
            Zwraca listę obiektów (instancji) klasy `cls`.
            Klasa musi implementować metodę init() zdolną przetworzyć wartości wejściowe
            i zasilić pola modelu.
        """
        return [cls(fields_values=row) for row in cls.all()]

    @classmethod
    def items(cls):
        """
            Pobiera z bazy danych uproszczoną (sformatowaną) listę rekordów.
        """
        raise NotImplementedError


class BaseModel(BaseDbModel):
    """
        Bazowy model danych.
    """

    verbose_name = None
    fields = None
    name = None

    def __init__(self, verbose_name=None, name=None, fields_values=None):
        self.verbose_name = verbose_name
        self.name = name
        # każda instancja musi zawierać swój zestaw pól
        self.fields = deepcopy(type(self).fields)
        if fields_values:
            self._init(fields_values)

    def _init(self, fields_values):
        """
            Inicjuje obiekt z danymi z BD.
        """
        for field_name, value in fields_values:
            if field_name == 'id':
                # w przypadku id (klucz główny w tabeli)
                # wartość powiązana jest z modelem, a nie polami
                self._id = value
            else:
                field = self.get_field(field_name)
                field.set_value(value)

    def add_new(self):
        """
            Tworzy i zapisuje nowy obiekt modelu.
            Wraca id obiektu (pk z tabeli z BD)
        """
        self.read_data()
        self._save_data()
        return self._id

    def update_model(self):
        """
            Aktualizuje istniejący model.
        """
        self.read_data()
        self._update_data()

    def get_field(self, name):
        """
            Zwraca obiekt pola o podanej nazwie.
        """
        for field in self.fields:
            if field.name == name:
                return field
        raise FieldNotFound

    def read_data(self):
        """
            Pobiera od użytkownika dane formularza.
        """
        for field in self.fields:
            field.read_data()

    def __str__(self):
        return self.verbose_name

    def verbose_details(self):
        """
            Zwraca rozbudowaną tekstową reprezentację modelu.
        """
        text_lines = [
            '{0}: {1}'.format(field.verbose_name, field.get_value()) for field in self.fields
        ]
        return '\n'.join(text_lines) + '\n'

    def set_data(self, data):
        """
            Ustawia wartości pól formularza na podstawie słownika {nazwa_pola: wartość}.
        """
        for field_name in data:
            try:
                field = self.get_field(field_name)
            except FieldNotFound:
                pass
            else:
                # waliduje i zapisuje wartość pola
                field.set_value(field._validate(data[field_name]))
        self._save_data()
