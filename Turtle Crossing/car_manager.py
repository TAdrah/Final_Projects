from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:
    def __init__(self):
        self.speed = STARTING_MOVE_DISTANCE
        self.list_of_cars = []
        self.create_it()

    def increase_speed(self):
        self.speed += MOVE_INCREMENT

    def move_it(self):
        for i in self.list_of_cars:
            i.forward(self.speed)

    def create_it(self):
        car = Turtle(shape="square")
        car.penup()
        car.shapesize(stretch_wid=1, stretch_len=2)
        car.color(random.choice(COLORS))
        car.goto(310, random.randint(-250, 250))
        car.setheading(180)
        self.list_of_cars.append(car)



