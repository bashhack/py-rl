""" Exception Handlers:

- custom exception handlers

"""


class RLError(Exception):
    """ Base class for domain-specific errors

    """


class EntityError(RLError):
    """ Entity error handling

    """
