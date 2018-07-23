# -*- coding: utf-8 -*-

from flask import Flask
from amelia.config import Config

amelia = Flask(
    __name__,
    static_url_path='',
    static_folder=Config().static_path,
)
amelia.config.from_object(Config)

from amelia import routes
