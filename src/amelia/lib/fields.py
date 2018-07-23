# -*- coding: utf-8 -*-

"""
    Biblioteka prototypów pól formularzy
"""


class UndefinedValue(object):
    """
        Klasa reprezentująca wartość nieokreśloną.
    """
    pass


class ValueNotSet(ValueError):
    """
        Wyjątek do obsługi dostępu do wartości nieustawionej.
    """
    pass


class ValidationError(ValueError):
    """
        Generyczny wyjątek do obsługi zdarzeń walidacji danych.
    """
    pass


class ValueRequired(ValidationError):
    """
        Wyjątek do obsługi wymagalności pola.
    """
    pass


class InvalidLength(ValidationError):
    """
        Wyjątek do obsługi walidacji długości danych.
    """
    pass


class Field(object):
    """
        Bazowy model pola.
    """

    _value = UndefinedValue
    name = None  # nazwa pola w bazie danych
    verbose_name = None
    default = None
    required = True
    help_text = None
    editable = True

    def __init__(self, **kwargs):
        """
            W bazowej implementacji hurtowo ustawia podane atrybuty obiektu.
        """
        for param_name in kwargs:
            setattr(self, param_name, kwargs[param_name])

    def get_value(self):
        """
            Zwraca wartość pola.
            Rzuca wyjątek ValueNotSet, jeśli na polu nie została ustawiona wartość.
        """
        if self._value is UndefinedValue:
            raise ValueNotSet
        return self._value

    def get_db_value(self):
        """
            Zwraca wartość pola znormalizowaną do zapisania w bazie danych.
            Domyślna implementacja zwraca self.get_value()
        """
        return self.get_value()

    def set_value(self, value):
        """
            Ustawia wartość na polu.
        """
        self._value = value

    def read_data(self):
        """
            Pobiera od użytkownika dane i ustawia wartość pola.
        """
        prompt = '{0}: '.format(self.verbose_name)
        raw_value = input(prompt)
        self.set_value(self._validate(raw_value))

    def _validate(self, value):
        """
            Bazowa walidacja wartości. Sprawdza wymagalność pola.
            W implementacjach potomnych należy wywołać metodą za pomocą funkcji super()
            Funkcja w przypadku napotkania błędu powinna rzucić wyjatek klasy/podklasy ValidationError.

            Zwraca wartość znormalizowaną gotową do ustawienia jako wartość pola.
        """
        if self.required and not value:
            raise ValueRequired("Value is required")
        return value
