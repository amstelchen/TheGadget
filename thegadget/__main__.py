import pygame
from .game import Game
from .intro import Intro

def main():
    pygame.init()
    Intro()
    app = Game()
    # app.window.after(1000, app.updateDisplay)
    #app.updateDisplay()
    #app.window.mainloop()

if __name__ == "__main__":
    main()