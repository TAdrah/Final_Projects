from turtle import Turtle
FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.score = 0
        self.goto(-280, 250)
        self.hideturtle()
        self.update_scoreboard()

    def update(self):
        self.score += 1
        self.clear()
        self.update_scoreboard()
        print(f'score is now {self.score}')

    def update_scoreboard(self):
        self.write(f"Score: {self.score}", font=FONT, align="left")

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=FONT)
