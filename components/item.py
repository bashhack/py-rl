""" Item:

- an item that can be picked up by an Entity

"""


class Item:
    """ A component that represents an object that can be picked up

    """

    def __init__(
        self, use_function=None, targeting=False, targeting_message=None, **kwargs
    ):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
