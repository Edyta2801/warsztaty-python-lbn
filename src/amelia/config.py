# -*- coding: utf-8 -*-

import os
import yaml
from amelia.lib.models import Singleton


class Config(Singleton):
    """
        Klasa dostarczająca konfigurację statyczną aplikacji.
    """
    app_dir = None  # katalog roboczy aplikacji
    app_db = None  # ścieżka do pliku bazy danych
    static_path = None
    SECRET_KEY = None
    TITLE = None
    static_config = None

    def __init__(self):
        if not Config.app_dir:
            Config.app_dir = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
            Config.app_db = os.path.join(Config.app_dir, 'db', 'amelia_db.sqlite')
            Config.static_path = os.path.join(Config.app_dir, 'amelia', 'static')
            # @FIXME: dopisać odczytywanie konfiguracji statycznej z pliku yaml
