from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("turtle")
        self.starting_position = STARTING_POSITION
        self.goto(self.starting_position)
        self.setheading(90)
        self.finish_line = FINISH_LINE_Y




    def go_up(self):
        self.forward(MOVE_DISTANCE)


    def next_level(self):
        print(f"hi, {self.ycor()}")
        if self.ycor() >= self.finish_line:
            self.goto(self.starting_position)
            print(f'im in next level, {self.position}')







