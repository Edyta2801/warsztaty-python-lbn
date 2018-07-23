"""
    Modele wbudowane i prototypy.
"""


class Singleton(object):
    """
        Prototyp singletona zapewniający jedną instancję klasy.
    """
    _singleton_instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._singleton_instance, cls):
            cls._singleton_instance = object.__new__(cls, *args, **kwargs)
        return cls._singleton_instance
