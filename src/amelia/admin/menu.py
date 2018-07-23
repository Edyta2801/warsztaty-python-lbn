"""
    Moduł obsługujący konsolowe menu administracyjne.
"""

from amelia.lib.menu import (
    GenericMenu,
    AddEvent,
    ShowEvents,
    ShowRegistartions,
    GenerateReport,
    ExitAppMenu,
)


class AdminMenu(GenericMenu):
    """
        Menu główne konsolowego interfejsu administracyjnego.
    """

    ADMIN_MENU = [
        AddEvent('1'),
        ShowEvents('2'),
        ShowRegistartions('3'),
        GenerateReport('4'),
        ExitAppMenu('0')
    ]
    header_text = 'Menu główne:'
