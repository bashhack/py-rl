""" Rectangle:

- create rooms

"""


class Rect:
    """ Creates a rectangle of dimenions (w/h) at position (x/y)

    """

    def __init__(self, x_pos, y_pos, width, height):
        self.x_1 = x_pos
        self.y_1 = y_pos
        self.x_2 = x_pos + width
        self.y_2 = y_pos + height

    def center(self):
        center_x = int((self.x_1 + self.x_2) / 2)
        center_y = int((self.y_1 + self.y_2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        return (
            self.x_1 <= other.x_2
            and self.x_2 >= other.x_1
            and self.y_1 <= other.y_2
            and self.y_2 >= other.y_1
        )
