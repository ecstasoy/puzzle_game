import turtle


class Tile:
    def __init__(self, image, init_position, curr_position, callback=None):
        self.image = image
        self.init_position = init_position
        self.curr_position = curr_position
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.penup()
        self.tile_callback = callback

    def draw(self, x, y):
        if not self.turtle.isvisible():
            self.turtle.showturtle()

        turtle.register_shape(self.image)
        self.turtle.shape(self.image)
        self.turtle.goto(x, y)
        self.turtle.onclick(self.on_event)

    def on_event(self, x, y):
        if self.tile_callback is not None:
            self.tile_callback(self.curr_position)
