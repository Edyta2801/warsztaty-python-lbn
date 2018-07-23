# -*- coding: utf-8 -*-

"""
    Amelia: moduł główny do uruchamiania aplikacji.
"""

import sys

from amelia import amelia
from amelia.admin.admin_api import AdminApi
from amelia.config import Config

INFO_MESSAGE = """Witaj w programie Amelia {version}.
Użycie: python app.py [komenda]
Dostępne komendy:
    manage: uruchamia konsolowy panel administracyjny
    run: uruchamia interfejs webowy (Flask)
"""

RUN_ADMIN_API_COMMAND = 'manage'
RUN_WEB_API_COMMAND = 'run'
UNKNOWN_COMMAND_EXIT_CODE = 1

if __name__ == '__main__':
    config = Config()
    try:
        command = sys.argv[1]
    except IndexError:
        print(INFO_MESSAGE.format(version=config.static_config['version']))
    else:
        if command == RUN_ADMIN_API_COMMAND:
            api = AdminApi()
            api()
        elif command == RUN_WEB_API_COMMAND:
            amelia.run(host=config.static_config['host'], port=int(config.static_config['port']))
        else:
            print('{0}: nieznana komenda'.format(command))
            sys.exit(UNKNOWN_COMMAND_EXIT_CODE)
