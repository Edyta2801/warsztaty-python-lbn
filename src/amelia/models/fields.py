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
        value = super(TextField, self)._validate(value)
        if len(value) < self.min_length or len(value) > self.max_length:
            raise InvalidLength("Maximal length exceeded")
        return value


class EmailField(TextField):
    """
        Model pola tekstowego typu e-mail.
    """

    def _validate(self, value):
        value = super(EmailField, self)._validate(value)
        if '.' not in value and '@' not in value:
            # @TODO przepisać na wyreżenia regularne
            raise ValidationError("Wrong e-mail format")
        return value


class DateField(Field):
    """
        Model pola daty.
    """
    help = 'Data w formacie YYYY-MM-DD'
    _dateformat = '%Y-%m-%d'

    def _validate(self, value):
        value = super(DateField, self)._validate(value)
        try:
            datetime.strptime(value, self._dateformat)
        except (TypeError, ValueError):
            raise ValidationError("Wrong date format")
        return value


class AutoDateField(Field):
    """
        Model pola daty - w przypadku nie ustawienia wartości zwraca datę bieżącą.
    """
    def get_value(self):
        """
            Zwraca wartość pola.
            Rzuca wyjątek ValueNotSet, jeśli na polu nie została ustawiona wartość.
        """
        if self._value is UndefinedValue:
            return date.today().isoformat()
        return self._value


class IntegerField(Field):
    """
        Model pola liczbowego.
    """
    default = 0

    def _validate(self, value):
        value = super(IntegerField, self)._validate(value)
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValidationError("Not an integer")
