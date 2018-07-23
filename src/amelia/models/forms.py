# -*- coding: utf-8 -*-

"""
    Definicje modeli formularzy.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    Email,
)
from amelia.lib.db import (
    WithDb,
    MultiSelectQuery,
)
from amelia.lib.forms import BaseModel
from amelia.models.fields import (
    TextField,
    DateField,
    IntegerField,
    EmailField,
    AutoDateField,
)


class Event(BaseModel):
    """
        Model zdarzenia.
    """

    _SQL_TABLENAME = 'events'
    verbose_name = 'Zdarzenie'
    fields = [
        TextField(
            name='name',
            verbose_name='Nazwa zdarzenia',
            help='Nazwa, maksymalnie 35 znaków'
        ),
        DateField(
            name='start_date',
            verbose_name='Data rozpoczęcia',
        ),
        DateField(
            name='end_date',
            verbose_name='Data zakończenia',
        ),
        TextField(
            name='location',
            verbose_name='Miejsce',
            help='Nazwa, maksymalnie 35 znaków'
        ),
        IntegerField(
            name='slots',
            verbose_name='Liczba miejsc',
            help='Liczba dostępnych miejsc. Zero oznacza brak limitu',
            required=False,
        ),
        TextField(
            name='desc',
            verbose_name='Opis',
            help='Opis, maksymalnie 512 znaków',
            max_length=512
        ),
    ]

    def __str__(self):
        if self._id:
            return '[{0}] {1} - {2}'.format(
                self._id,
                self.get_field('name').get_value(),
                self.get_field('start_date').get_value()
            )
        return super(Event, self).__str__()

    @classmethod
    def items(cls):
        """
            Pobiera z bazy danych uproszczoną (sformatowaną) listę rekordów.
        """
        def unzip_row(row):
            """
                Rozcala jeden rekord do postaci do wyświetlenia.
            """
            row = list(row)
            return (
                str(row[0][1]), ' / '.join([row[1][1], row[2][1], row[4][1]])
            )

        with WithDb() as db:
            data_rows = db.get_many(
                MultiSelectQuery(cls._SQL_FETCH_MANY.format(table_name=cls._SQL_TABLENAME))
            )
        return [unzip_row(row) for row in data_rows]


class RegistrationForm(BaseModel):
    """
        Model formularza rejestracji.
    """
    _SQL_TABLENAME = 'registrations'
    fields = [
        IntegerField(
            verbose_name='Zdarzenie',
            name='event_id'
        ),
        TextField(
            name='first_name',
            verbose_name='Imię',
            help='Podaj imię, maksymalnie 35 znaków.'
        ),
        TextField(
            name='last_name',
            verbose_name='Nazwisko',
            help='Podaj nazwisko, maksymalnie 35 znaków.'
        ),
        EmailField(
            name='email',
            verbose_name='Adres e-mail',
            help='Podaj poprawny adres e-mail'
        ),
        AutoDateField(
            name='registration_date',
            verbose_name='Data rejestracji',
        ),
    ]

    def __str__(self):
        if self._id:
            return '[{0}] {1} - {2}: {3}'.format(
                self._id,
                self.get_field('first_name').get_value(),
                self.get_field('last_name').get_value(),
                self.get_field('registration_date').get_value()
            )
        return super(Event, self).__str__()


_data_required_message = 'To pole jest wymagane'
_wrong_email = 'Podaj poprawny adres e-mail'


class WebRegistrationForm(FlaskForm):
    """
        Webowy formularz rejestracji (Flask).
    """
    event_id = SelectField('Zdarzenie', choices=[])
    first_name = StringField(
        'Imię', validators=[DataRequired(message=_data_required_message)]
    )
    last_name = StringField(
        'Nazwisko', validators=[DataRequired(message=_data_required_message)]
    )
    email = StringField(
        'Adres e-mail', validators=[Email(message=_wrong_email)]
    )
    submit = SubmitField('Wyślij')
