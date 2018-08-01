# -*- coding: utf-8 -*-

"""
    Definicje pól do budowy formularzy dla interfejsu administracji.
"""

from datetime import (
    datetime,
    date,
)

from amelia.lib.fields import (
    Field,
    InvalidLength,
    ValidationError,
    UndefinedValue,
)


class TextField(Field):
    """
        Model pola tekstowego
    """
    default = ''
    max_length = 35
    min_length = 3

    def _validate(self, value):
        # @FIXME: dopisać walidację pola
        raise NotImplementedError


class EmailField(TextField):
    """
        Model pola tekstowego typu e-mail.
    """

    def _validate(self, value):
        # @FIXME: dopisać walidację pola
        raise NotImplementedError


class DateField(Field):
    """
        Model pola daty.
    """
    help = 'Data w formacie YYYY-MM-DD'
    _dateformat = '%Y-%m-%d'

    def _validate(self, value):
        # @FIXME: dopisać walidację pola
        raise NotImplementedError


class AutoDateField(Field):
    """
        Model pola daty - w przypadku nie ustawienia wartości zwraca datę bieżącą.
    """
    def get_value(self):
        """
            Zwraca wartość pola.
            Rzuca wyjątek ValueNotSet, jeśli na polu nie została ustawiona wartość.
        """
        # @FIXME: dopisać walidację pola
        raise NotImplementedError


class IntegerField(Field):
    """
        Model pola liczbowego.
    """
    default = 0

    def _validate(self, value):
        # @FIXME: dopisać walidację pola
        raise NotImplementedError
