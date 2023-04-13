from turtle import Turtle


STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Snake:
    def __init__(self):
        self.all_snakes = []
        self.create_snake()
        self.head = self.all_snakes[0]

    def create_snake(self):
        for position in STARTING_POSITIONS:
            self.add_snake(position)

    def add_snake(self, position):
        snake = Turtle(shape="square")
        snake.fillcolor("white")
        snake.pencolor("white")
        snake.penup()
        snake.goto(position)
        self.all_snakes.append(snake)

    def extend(self):
        self.add_snake(self.all_snakes[-1].position())

    def move(self):
        for snakes in range(len(self.all_snakes) - 1, 0, -1):
            new_x = self.all_snakes[snakes - 1].xcor()
            new_y = self.all_snakes[snakes - 1].ycor()
            self.all_snakes[snakes].goto(new_x, new_y)
        self.all_snakes[0].forward(MOVE_DISTANCE)

    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

