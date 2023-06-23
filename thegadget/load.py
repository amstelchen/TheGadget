import os
import io
import time
import pygame
import cairosvg  # noqa: E402


class Loader():
    def __init__(self, pos=None, scale=0.25):
        self.pos = pos
        self.scale = scale

        pygame.init()
        modes = pygame.display.list_modes()
        self.screen = pygame.display.set_mode(modes[0])
        pygame.display.toggle_fullscreen()
        # pygame.display.set_caption(FULLNAME)
        self.screen = pygame.display.get_surface()
        self.window = self.screen
        self.load()

    def load(self):
        svg_file_anim = os.path.join(os.path.dirname(__file__), "resources", "anim", "Little_Boy_internal_diagram.svg")
        self.svg_string = open(svg_file_anim, "rt").read()

    def show(self):
        step = 10
        posx_1a = 336
        posx_2a = 1010
        posx_3a = 275
        posx_2b = posx_2a + step
        posx_3b = posx_3a + step
        for state in range(posx_1a, 810, step):
            # print(self.svg_string)
            svg_bytes = self.svg_string.encode()
            png_out = io.BytesIO()
            cairosvg.svg2png(bytestring=svg_bytes, write_to=png_out, scale=self.scale)
            png_out.seek(0)
            self.surface_div = pygame.image.load(png_out, "png")
            if self.pos is None:
                self.pos = (25, self.screen.get_height() - 25 - self.surface_div.get_height())
            self.window.blit(self.surface_div, self.pos)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return 0

            pygame.display.flip()
            time.sleep(0.05)
            posx_1a = state
            posx_1b = posx_1a + step
            posx_2b = posx_2a + step
            posx_3b = posx_3a + step
            self.svg_string = self.svg_string.replace(f'rect id="bod" x="-{posx_1a}"', f'rect id="bod" x="-{posx_1b}"')
            self.svg_string = self.svg_string.replace(
                f'g id="seg" transform="matrix(-1 0 0 -.55 {posx_2a} 314)"',
                f'g id="seg" transform="matrix(-1 0 0 -.55 {posx_2b} 314)"')
            self.svg_string = self.svg_string.replace(f'path d="m{posx_3a} 137v-37m61 0v37"', f'path d="m{posx_3b} 137v-37m61 0v37"')
            posx_2a += step
            posx_3a += step
            # print(self.svg_string)


if __name__ == '__main__':
    loader = Loader(scale=0.4)
    loader.load()
    loader.show()
