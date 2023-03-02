import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
car_manager = CarManager()
scoreboard = Scoreboard()
counter = 0

screen.listen()
player = Player()
screen.onkey(player.go_up, "Up")


game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

#   create car every 6th loop, +1 to counter, then move car forward
    if counter % 6 == 0:
        car_manager.create_it()
    counter +=1
    car_manager.move_it()

#   detect collision with car
    for x in car_manager.list_of_cars:
        if player.distance(x) < 20:
            game_is_on = False
            scoreboard.game_over()

#   check if user cleared the level, reset screen, score ++, cars go faster
    if player.ycor() > player.finish_line:
        scoreboard.update()
        car_manager.increase_speed()
        player.next_level()

screen.exitonclick()
