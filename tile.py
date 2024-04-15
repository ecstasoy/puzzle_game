import turtle


class Tile:
    """
    A class that represents tiles in Board (board of the game)

    Attributes:
        image (str): The image file path of the tile
        init_position (tuple): The initial position of the tile
        curr_position (tuple): The current position of the tile
        turtle (turtle): A turtle object used for drawing, representing an image registered as a shape
        tile_callback (function): Callback function on the event of click
    """
    def __init__(self, image, init_position, curr_position, callback=None):
        """
        Initialize a Tile object
        :param image: The image file path of the tile
        :param init_position: The initial position of the tile
        :param curr_position: The current position of the tile
        :param callback: Callback function on the event of click, initialized as None
        """
        self.image = image
        self.init_position = init_position
        self.curr_position = curr_position
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.penup()
        self.tile_callback = callback

    def draw(self, x, y):
        """
        Draw the tile at the given position (x, y)
        :param x: x-coordinate of the click
        :param y: y-coordinate of the click
        :return: None
        """
        if not self.turtle.isvisible():
            self.turtle.showturtle()

        turtle.register_shape(self.image)
        self.turtle.shape(self.image)
        self.turtle.goto(x, y)
        self.turtle.onclick(self.on_event)

    def on_event(self, x, y):
        """
        Callback function on the event of click
        :param x: x-coordinate of the click
        :param y: y-coordinate of the click
        :return: None
        """
        if self.tile_callback is not None:
            self.tile_callback(self.curr_position)
