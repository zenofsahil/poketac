class PokeAPIException(Exception):
    """ Top level exception class for our application
    """
    pass

class PokemonAPIException(PokeAPIException):
    """ Exception class for any errors related to the pokemon api
    """
    pass

class TranslationAPIException(PokeAPIException):
    """ Exception class for any errors related to the translation api
    """
    pass

class PokemonAPIHTTPException(PokemonAPIException):
    """ Exception class for HTTP related exceptions for the pokemon api
    """
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail

class TranslationAPIHTTPException(TranslationAPIException):
    """ Exception class for HTTP related exceptions for the translation api
    """
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
