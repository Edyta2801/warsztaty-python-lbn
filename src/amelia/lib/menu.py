# -*- coding: utf-8 -*-

import os
import sys
import csv

from amelia.config import Config
from amelia.models.forms import (
    Event,
    RegistrationForm,
)


class MenuExit(Exception):
    """
        Wyjątek do obsługi powrotu w menu (wyjście do poprzedniego menu przy level=1)
        Pozwala na sterownie, o ile poziomów w górę drzewa ma nastąpić powrót.
    """
    level = 1

    def __init__(self, level=1):
        self.level = level


class ObjectAsMenu(object):
    """
        Adapter - klasa typu proxy pozwlająca na operacje na obiekcie
        instancji BaseModel jak na pozycji menu.
    """
    _model = None
    index = None
    view_only = False

    def __init__(self, model, view_only=False):
        self._model = model
        self.index = str(model._id)
        self.view_only = view_only

    def __str__(self):
        return str(self._model)

    def __call__(self, parent):
        """
            Uruchamia menu pozwalające na zarządzanie obiektem.
            Jeśli obiekt stworzono z flagą view_only=True, do menu nie zostaną
            załączone komendy pozwalające na edycję.
        """
        if self.view_only:
            menu_items = [ReturnMenu('0')]
        else:
            menu_items = [
                EditEvent('1', related_object=self._model),
                DeleteEvent('2', related_object=self._model),
                ReturnMenu('0')
            ]
        context_menu = GenericMenu(
            menu_items=menu_items,
            header_text=self._model.verbose_details()
        )
        context_menu()


class MenuItem(object):
    """
        Atomowa pozycja menu.
    """
    MENU_ITEM_TEMPLATE = '[{0}] {1}'

    _related_object = None  # zapewnia dostęp do powiązanego obiektu

    verbose_name = None  # nazwa wyświetlana
    index = None  # symbol pozycji (indeksu/klucza) w menu

    def __init__(self, index, related_object=None):
        self.index = index
        if related_object:
            self._related_object = related_object

    def __str__(self):
        """
            Wyświetla statyczny literał `[symbol] nazwa`.
        """
        return self.MENU_ITEM_TEMPLATE.format(self. index, self.verbose_name)

    def __call__(self, parent):
        """
            Uruchamia logikę obsługującą daną pozycję menu.
            Otrzymuje obiekt rodzica (menu), na którym może np. ustawiać wiadomości.
        """
        raise NotImplementedError


class AddEvent(MenuItem):
    verbose_name = 'Dodaj zdarzenie'

    def __call__(self, parent):
        _id = Event().add_new()
        if _id is not None:
            parent.set_message('Dodano nowy obiekt: {0}'.format(_id))


class ShowEvents(MenuItem):
    verbose_name = 'Wyświetl zdarzenia'

    def __call__(self, parent):
        events = Event.load_many()
        events = [ObjectAsMenu(event) for event in events]
        events.append(ReturnMenu('0'))
        object_menu = GenericMenu(
            menu_items=events,
            header_text='Wybierz zdarzenie:'
        )
        object_menu()


class ShowRegistartions(MenuItem):
    verbose_name = 'Wyświetl rejestracje'

    def __call__(self, parent):
        regs = RegistrationForm.load_many()
        regs = [ObjectAsMenu(reg, view_only=True) for reg in regs]
        regs.append(ReturnMenu('0'))
        object_menu = GenericMenu(
            menu_items=regs,
            header_text='Wybierz rejestrację:'
        )
        object_menu()


class ReturnMenu(MenuItem):
    verbose_name = 'Powrót'

    def __call__(self, parent):
        raise MenuExit


class EditEvent(MenuItem):
    verbose_name = 'Edytuj zdarzenie'

    def __call__(self, parent):
        self._related_object.update_model()
        parent.set_message('Obiekt zmodyfikowano')
        raise MenuExit


class DeleteEvent(MenuItem):
    verbose_name = 'Usuń zdarzenie'

    def __call__(self, parent):
        self._related_object.delete()
        del self._related_object
        parent.set_message('Obiekt usunięto')
        raise MenuExit(level=2)


class GenerateReport(MenuItem):
    verbose_name = 'Wykonaj raport'

    def __call__(self, parent):
        """
            Eksportuje rekordy rejestracji do pliku CSV.
        """
        # @FIXME: dopisać generowanie raportu do pliku CSV


class ExitAppMenu(MenuItem):
    verbose_name = 'Zakończ program'

    def __call__(self, parent):
        sys.exit(0)


class GenericMenu(object):
    ADMIN_MENU = None  # lista obiektów MenuItem
    PROMT_MESSAGE = '->'
    message = ''
    header_text = ''

    def __init__(self, menu_items=None, header_text=None):
        if menu_items:
            self.ADMIN_MENU = menu_items
        if header_text:
            self.header_text = header_text

    def __getitem__(self, index):
        """
            Adaptuje interfejs słownika, pozwala na wybieranie elementów po kluczu.
        """
        # @FIXME: dopisać implementację słownika pozwalająca na wybieranie menu[obiekt]
        raise NotImplementedError

    def __call__(self):
        while True:
            self.read()
        # @FIXME: dopisać obsługę cofania się w menu (obsługa MenuExit)

    def _clear_screen(self):
        """
            Czyści ekran systemowym wywołąniem.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def _show_menu(self):
        """
            Wyświetla strukturę menu.
        """
        if self.message:
            print(self.message)
            print()
            self.message = ''
        print(self.header_text)
        for item in self.ADMIN_MENU:
            print(item)

    def set_message(self, message):
        """
            Dodaje nową wiadomość, która zostanie wyświetlona jednorazowo ponad menu.
        """
        self.message = message

    def read(self):
        """
            Wyświetla elementy bieżącego menu, odczytuje wybór użytkownika
            i uruchamia akcję podpiętą pod daną pozycję.
        """
        self._clear_screen()
        self._show_menu()
        user_choice = input(self.PROMT_MESSAGE)
        try:
            selected_item = self[user_choice]
        except KeyError:
            pass
        else:
            try:
                selected_item(self)
            except KeyboardInterrupt:
                self.set_message('Operacja anulowana')
