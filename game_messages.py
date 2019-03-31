""" Messages:

- message
- message log

"""

import textwrap

import tcod


class Message:
    """ Basic abstraction for a message (text and color)

    """

    def __init__(self, text, color=tcod.white):
        self.text = text
        self.color = color


class MessageLog:
    """ Collection of messages, as well as a reference to their position

    """

    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        """ Adds a message to the message log (with display formatting)

        """

        # Split the message across multiple lines, if necessary
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))
