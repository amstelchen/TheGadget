import os
import sys
import logging

import pygame
# hack for better fonts on linux
if sys.platform == 'linux':
    import pygame_menu

from pygame.locals import Color

from .__version__ import __appname__, __description_short__, __studioname__
#from colors import *
musicloop = os.path.join(os.path.dirname(__file__), 'resources', 'music', 'The-Games_Looping.mp3')


class Intro():
    def __init__(self):

        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        self.run()

    def close_game(self):
        print("Beendet.")
        #pygame.quit()
        self.run = False
        #quit()

    def run(self):

        #pygame.init()

        pygame.font.init()
        clock = pygame.time.Clock()

        boldfont = pygame.font.SysFont("Arial Black", 14)
        largefont = pygame.font.SysFont("Arial Black", 80)
        mediumfont = pygame.font.SysFont("Arial Black", 40)

        alpha = 0
        alpha_change = 1

        #ScreenX = 1920
        #ScreenY = 1080

        modes = pygame.display.list_modes()
        screen = pygame.display.set_mode(modes[0])
        pygame.display.toggle_fullscreen()

        #screen = pygame.display.set_mode((ScreenX, ScreenY))

        logging.debug(f"Available modes: {[mode for mode in modes]}")
        logging.debug(f"Selected mode: {pygame.display.get_window_size()}")

        screen.fill(Color("black"))
        imgStudio = largefont.render(__studioname__, True, Color("white"))
        imgPresents = mediumfont.render(("presents"), True, Color("white"))

        if sys.platform == 'linux':
            font_riesig = pygame.font.Font(pygame_menu.font.FONT_OPEN_SANS_BOLD, 120)
        elif sys.platform == 'win32':
            font_riesig = pygame.font.SysFont("Open Sans bold", 120)
        text_riesig = font_riesig.render(f" {__appname__} ", True, Color("white"), Color("darkolivegreen"))

        box1 = pygame.Surface((text_riesig.get_width() + 100, text_riesig.get_height()))
        box1.blit(text_riesig, (0, 0))

        if sys.platform == 'linux':
            font_gross = pygame.font.Font(pygame_menu.font.FONT_OPEN_SANS_BOLD, 32)
        elif sys.platform == 'win32':
            font_gross = pygame.font.SysFont("Open Sans bold", 32)
        text_gross = font_gross.render(f"{__description_short__.upper()}", True, (255, 255, 255), Color("darkolivegreen"))

        box2 = pygame.Surface((text_riesig.get_width(), text_gross.get_height()))
        box2.fill(Color("darkolivegreen"))
        box2.blit(text_gross, ((text_riesig.get_width() - text_gross.get_width()) / 2, 0))

        pygame.mixer_music.load(musicloop, "mp3")  # "ogg")
        #if audiostate == 1:
        pygame.mixer_music.play(-1)

        run = True
        while run:

            clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    #close_game()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x and event.mod == pygame.KMOD_CTRL:
                        #pygame.quit()
                        pass
                        #sys.exit()
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_f:
                        pygame.display.toggle_fullscreen()

            alpha += alpha_change
            if not 0 <= alpha <= 255:
                alpha_change *= -1
            #else:
            #    run = False
            alpha = max(0, min(alpha, 255))
            #print(alpha)

            if alpha == 0:
                #pygame.quit()
                run = False

            screen.fill(0)

            alphaimgStudio = imgStudio.copy()
            alphaimgStudio.set_alpha(alpha)
            alphaimgPresents = imgPresents.copy()
            alphaimgPresents.set_alpha(alpha)

            screen.blit(alphaimgStudio, (screen.get_width() / 2 - imgStudio.get_width() / 2,
                screen.get_height() / 2 - imgStudio.get_height() / 2))
            screen.blit(alphaimgPresents, (screen.get_width() / 2 - imgPresents.get_width() / 2,
                screen.get_height() / 2 - imgPresents.get_height() / 2 + 100))

            pygame.display.flip()

        alpha_change = 1
        alpha = 0

        pygame.event.clear(pygame.KEYDOWN, True)
        events = None
        #pygame.time.delay(500)

        #pygame.mixer_music.play(-1)

        run = True
        while run:

            clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    #close_game()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        alpha = 255
                        #final = True
                        run = False

            alpha += alpha_change
            #if not 0 <= alpha <= 255:
            #    alpha_change *= -1
            #else:
            #    run = False
            alpha = max(0, min(alpha, 255))
            #print(alpha)

            if alpha == 255:
                #pygame.quit()
                run = False

            screen.fill(0)

            alpha_image = box1.copy()
            alpha_image.set_alpha(alpha)
            #screen.blit(alpha_image, (0, 0))
            screen.blit(alpha_image, (screen.get_width() / 2 - text_riesig.get_width() / 2,
                screen.get_height() / 2 - text_riesig.get_height() / 2))

            pygame.display.flip()

        alpha = 0
        alpha_change = 1

        pygame.event.clear()

        run = True
        while run:

            #if final == True:
            #    alpha = 255

            clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.close_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        alpha = 255
                        run = False

            alpha += alpha_change
            #if not 0 <= alpha <= 255:
            #    alpha_change *= -1
            #else:
            #    run = False
            alpha = max(0, min(alpha, 255))
            #print(alpha)

            if alpha == 255:
                #pygame.time.delay(3000)
                run = False

            alpha_image2 = box2.copy()
            alpha_image2.set_alpha(alpha)    
            screen.blit(alpha_image2, (screen.get_width() / 2 - text_riesig.get_width() / 2,
                screen.get_height() / 2 + text_riesig.get_height() / 2))
            pygame.display.flip()
