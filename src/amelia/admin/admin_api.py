"""
    Moduł obsługi interfejsu administracyjnego.
"""

from amelia.admin.menu import AdminMenu


class AdminApi(object):
    """
        Model konsolowego interfejsu do zarządzania danymi.
    """

    def __init__(self):
        self.menu = AdminMenu()

    def run(self):
        """
            Uruchamia menu i czeka na komendy użytkownika.
        """
        self.menu()

    def __call__(self):
        self.run()
