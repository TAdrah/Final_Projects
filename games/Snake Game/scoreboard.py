from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.sety(280)
        self.color("white")
        self.hideturtle()
        self.update_scoreboard()

    def update(self):
        self.score += 1
        self.clear()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(f"Score: {self.score}", align="center")

    def game_over(self):
        self.sety(0)
        self.write("GAME OVER", align="center")