import sys
import os
from pathlib import Path
import pygame
from pygame.image import load
from pygame.locals import Color
import datetime
import logging
# import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex, Normalize
from matplotlib.patches import Polygon
from matplotlib.colorbar import ColorbarBase
import matplotlib.backends.backend_agg as agg
import sqlite3
import io
#import pylab
import cairosvg
#from svg import Parser, Rasterizer
#from intro import Intro

from .__version__ import PROGNAME, FULLNAME, VERSION, AUTHOR, DESC, __appname__, __description_short__, __studioname__, __controls__
from .utils import Data, SVG


class Game():
    def __init__(self):
        self.config = {
            "window_width": 1212,
            "window_height": 769,
            "fg": "white",
            "bg": "black",
            "fontface": "Noto sans",
            "fontface_mono": "Noto sans Mono",
            "fontsize": "50",
            "fullscreen": 1
        }

        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        self.loadDefaults()

        data_file = os.path.join(os.path.dirname(__file__), 'resources', 'database', PROGNAME + ".db")
        loader = Data(data_file)
        dates_data = loader.load_table_data("Dates")
        people_data = loader.load_table_data("People")
        places_data = loader.load_table_data("Places")
        logging.debug(f"Loaded {len(dates_data)} dates, {len(people_data)} people, {len(places_data)} places.")
        #print(dates_data)

        # Print the loaded data
        #for row in dates_data:
        #    print(row)

#        self.window.bind("<F11>", self.quitNewYearsClock)
#        self.window.bind("<Escape>", self.quitNewYearsClock)

        # Initialize Pygame, now handled in main()
        #pygame.init()

        self.audiostate = True

        # Set up the game window
        # window_width = 800
        # window_height = 600
        #self.window = pygame.display.set_mode((self.config["window_width"], self.config["window_height"]))

        #modes = pygame.display.list_modes()
        #self.window = pygame.display.set_mode(modes[0], pygame.FULLSCREEN)
        
        self.fullScreenState = True
        #pygame.display.toggle_fullscreen()

        pygame.display.set_caption(FULLNAME)
        self.screen = pygame.display.get_surface()
        self.window = self.screen

        self.screen.fill(pygame.color.Color("white"))  # Fill the window with black color

        ff = self.config['fontface']
        ff_mono = self.config['fontface_mono']
        font_big = pygame.font.SysFont(ff, 36)
        font_med = pygame.font.SysFont(ff, 28)
        font_sml = pygame.font.SysFont(ff, 24)
        font_med_serif = pygame.font.SysFont(ff_mono, 28)
        font_sml_serif = pygame.font.SysFont(ff_mono, 24)

        svg_file_map = os.path.join(os.path.dirname(__file__), "resources", "maps", "Manhattan_Project_US_Canada_Map_C.svg")
        self.surface_map = pygame.image.load(svg_file_map)

        svg_file_pos = os.path.join(os.path.dirname(__file__), "resources", "maps", "Manhattan_Project_US_Canada_Map_D.svg")
        self.surface_pos = pygame.image.load(svg_file_pos)

        svg_string = SVG(places_data).create_markup()
        #logging.debug(str(svg_string))

        svg_file_div = os.path.join(os.path.dirname(__file__), "svgtest.svg")
        #self.surface_div = pygame.image.load(svg_file_div)
        #self.surface_div = pygame.image.load(io.BytesIO(svg_string.encode()))
        logging.debug("Images loaded.")

        #svg_io = io.BytesIO(svg_string.encode())
        #png_io = io.BytesIO()
        #with open(svg_file_div, "rb") as f:
        #    svg_cont = f.read()
        #    cairosvg.svg2png(file_obj=f, write_to=png_io)
        #    png_io.seek(0)
        #    self.surf = pygame.image.load(png_io, "png")

        #svg_io2 = io.BytesIO(svg_string.encode())
        #svg_io2 = bytes(svg_string.encode())
        svg_io2 = svg_string.encode()
        #svg_io2.seek(0, io.SEEK_END)
        png_io2 = io.BytesIO()

        cairosvg.svg2png(bytestring=svg_io2, write_to=png_io2)
        png_io2.seek(0)
        self.surface_div = pygame.image.load(png_io2, "png")

        bg_color = (0, 0, 0)   # fill red as background color
        #screen.fill(bg_color)
        #screen.blit(surf, (0, 0)) # x, y position on screen
        #pygame.display.flip()

        # Game variables
        running = True
        logging.debug("Setting up clock...")
        clock = pygame.time.Clock()

        self.newsurf = pygame.Surface((500, 500))
        self.newsurf.fill(Color("mediumaquamarine"))
        self.blit_text(self.newsurf, FULLNAME, (25, 25), font_med, color=Color("black"))
        self.blit_text(self.newsurf, DESC, (25, 75), font_sml, color=Color("black"))
        self.screen.blit(self.newsurf, (100, 100))

        self.newsurf = pygame.Surface((500, 300))
        self.newsurf.fill(Color("mediumaquamarine"))
        self.blit_text(self.newsurf, "Controls", (25, 25), font_med, color=Color("black"))
        self.blit_text(self.newsurf, __controls__, (25, 75), font_sml_serif, color=Color("black"))
        self.screen.blit(self.newsurf, (self.screen.get_width() - 600, self.screen.get_height() - 600))

        self.newsurf = pygame.Surface((500, 75))
        self.newsurf.fill(Color("mediumaquamarine"))
        self.blit_text(self.newsurf, "Press space to continue", (25, 25), font_sml, color=Color("black"))
        self.screen.blit(self.newsurf, (self.screen.get_width() - 600, self.screen.get_height() - 200))

        pygame.display.flip()
        self.screen.fill((255,255,255))

        # Fictional date
        start_date = datetime.date(1941, 10, 9)
        start_date = datetime.date(1942, 6, 24)
        start_date = datetime.date(1942, 11, 30)
        start_date = datetime.date(1939, 8, 1)
        atest_date = datetime.date(1945, 7, 16)
        final_date = datetime.date(1947, 8, 15)
        current_date = datetime.date(2023, 5, 24)
        current_date = start_date
        days_gone = 0

        # Game loop
        while running:
            #plt.show()

            self.text_hist = ""

            self.text = font_sml.render(f"Current Date: {current_date}", True, (0, 0, 0), Color("mediumaquamarine"))
            self.text_rect = self.text.get_rect(center=(self.window.get_width() // 2 + 100, self.window.get_height() - 50))
            #text.fill(pygame.color.Color("mediumaquamarine"))

            self.updateDisplay()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # checking if keydown event happened or not
                if event.type == pygame.KEYDOWN:
                    
                    # checking if key "F" was pressed
                    if event.key == pygame.K_f:
                        logging.debug("Key F has been pressed")
                        if self.fullScreenState:
                            self.quitFullScreen(event)
                        else:
                            self.toggleFullScreen(event)
                        self.updateDisplay()
                    
                    # checking if key "A" was pressed
                    if event.key == pygame.K_a:
                        logging.debug("Key A has been pressed")
                    
                    # checking if key "W" was pressed
                    if event.key == pygame.K_w:
                        logging.debug("Key W has been pressed")
                        days_gone += 7
                    
                    # checking if key "Q" was pressed
                    if event.key == pygame.K_q:
                        logging.debug("Key Q has been pressed")
                        running = False
                    
                    # checking if key "M" was pressed
                    if event.key == pygame.K_m:
                        logging.debug("Key M has been pressed")
                        if self.audiostate is True:
                            pygame.mixer_music.stop()
                            self.audiostate = False
                        else:
                            pygame.mixer_music.play(-1)
                            self.audiostate = True

                    # checking if key "M" was pressed
                    if event.key == pygame.K_SPACE:
                        logging.debug("Space has been pressed")
                        days_gone += 1

                    current_date = start_date + datetime.timedelta(days=days_gone)
                    logging.debug(current_date)
                    #print(current_date.strftime("%Y-%m-%d"))
                        #print(type(dates_data))

                    for date_event in dates_data:
                        if current_date.strftime("%Y-%m-%d") == date_event[1]:
                            logging.debug("Date event found!")
                            self.text_hist = f"{date_event[1]}\n{date_event[2]}"
                            self.subtext = f"{date_event[3]}"
                            self.newsurf = pygame.Surface((500, 500))
                            self.newsurf.fill(Color("mediumaquamarine"))
                            self.blit_text(self.newsurf, self.text_hist, (25, 25), font_med, color=Color("black"))
                            self.blit_text(self.newsurf, self.subtext, (25, 150), font_sml, color=Color("black"))
                            self.screen.blit(self.newsurf, (100, 100))
                        else:
                            pygame.display.flip()
                        # self.updateDisplay()

                    for people_event in people_data:
                        if current_date.strftime("%Y-%m-%d") == people_event[5]:
                            logging.debug("Person event found!")
                            self.text_hist = f"{people_event[5]}\n{people_event[1]} joined the Manhattan Project."
                            self.subtext = f"{people_event[4]}"
                            self.newsurf = pygame.Surface((500, 800))
                            self.newsurf.fill(Color("mediumaquamarine"))
                            charRect = pygame.Rect((270,10),(10, 10))
                            charImage = load(os.path.join(os.path.dirname(__file__), 'resources', 'images', people_event[1] + '.png'))
                            ratio = charImage.get_height()/charImage.get_width()
                            charImage = pygame.transform.scale(charImage, (220, 220 * ratio))
                            charImage = charImage.convert()
                            self.newsurf.blit(charImage, charRect)
                            self.blit_text(self.newsurf, self.text_hist, (25, 25), font_sml, color=Color("black"))
                            self.blit_text(self.newsurf, self.subtext, (25, 280), font_sml, color=Color("black"))
                            self.screen.blit(self.newsurf, (self.screen.get_width() - 600, 100))
                        else:
                            pygame.display.flip()

            # Update game logic

            # Render the game

            #surface = pygame.image.load('Manhattan_Project_US_Canada_Map_2.svg')
            #surface = pygame.transform.smoothscale(surface, (screen.get_width(), screen.get_height()))
            #screen.blit(surface, (0, 0))


            # Render SVG to Pygame surface using Pycairo
            #surface = cairosvg.surface.PNGSurface.from_file(svg_file)
            #with open(svg_file, "rb") as f:
            #    surface = cairosvg.surface.PNGSurface.convert(f)
            #    stream = io.BytesIO(surface.to_png())
            #    image = pygame.image.load(stream)

            #pygame.display.flip()

            #screen.blit(surf, (0, 0)) # x, y position on screen

            #pygame.display.flip()  # Update the window
            #self.updateDisplay()

            # Control the frame rate
            clock.tick(10)  # Cap the frame rate at 60 FPS

        # Quit the game
        logging.debug("Quitting.")
        pygame.quit()

    def updateDisplay(self):
        self.screen.fill((255,255,255))
        #self.screen.fill(pygame.color.Color("mediumaquamarine"))

        # Display the fictional date
        self.window.blit(self.text, self.text_rect)

        self.screen.blit(self.surface_map, (0, 0))
        self.screen.blit(self.surface_pos, (0, 0))
        self.screen.blit(self.surface_div, (0, 0))

        #pygame.display.flip()

        #if self.newsurf is not None:
        if len(self.text_hist) > 0:
        #if isinstance(self.newsurf, pygame.Surface):
            self.screen.blit(self.newsurf, (0, 0), )
        else:

        # Update the window
        #logging.debug("Update the window")
            pass
            #self.screen.fill((255,255,255))
        #pygame.display.flip()  

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        #self.window.attributes("-fullscreen", self.fullScreenState)
        pygame.display.set_mode((self.config["window_width"], self.config["window_height"]), pygame.FULLSCREEN)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        #self.window.attributes("-fullscreen", self.fullScreenState)
        pygame.display.set_mode((self.config["window_width"], self.config["window_height"]), pygame.RESIZABLE)

    def loadDefaults(self):
        if os.sys.platform == 'win32':
            if os.path.isdir(os.path.join(os.environ['LOCALAPPDATA'])):
                userPath = os.path.join(os.environ['LOCALAPPDATA'], PROGNAME, 'settings.conf')
        if sys.platform == 'linux':
            userPath = str(Path('~').expanduser()) + "/.config/" + PROGNAME + "/settings.conf"
        try:
            with open(userPath, "r") as configFile:
                # self.config= configFile.readlines()
                # print(self.config)
                self.config = {}
                for configLine in configFile.readlines():
                    name, value = configLine.strip().split(" = ")
                    self.config[name] = value
                #print(self.config)
        except FileNotFoundError as e:
            logging.warning(e)
            logging.warning("Using sane defaults.")

    def blit_text(self, surface, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.


class Map():
    def __init__(self):
        matplotlib.use("Agg")

        fig, ax = plt.subplots()

        #fig = plt.figure() # figsize=(5, 5), dpi=20, frameon=False)
        #ax = plt.Axes(fig, [0., 0., 1., 1.])
        #ax.margins(x=0, y=0, tight=True)

        # Lambert Conformal map of lower 48 states.
        m = Basemap(llcrnrlon=-119,llcrnrlat=20,urcrnrlon=-64,urcrnrlat=49,
                    projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

        # Mercator projection, for Alaska and Hawaii
        m_ = Basemap(llcrnrlon=-190,llcrnrlat=20,urcrnrlon=-143,urcrnrlat=46,
                    projection='merc',lat_ts=20)  # do not change these numbers

        ## data from U.S Census Bureau
        ## http://www.census.gov/geo/www/cob/st2000.html
        shp_info = m.readshapefile('/raid/Projekte/TheGadget/st99_d00','states',drawbounds=True,
                                linewidth=0.45,color='gray')
        shp_info_ = m_.readshapefile('st99_d00','states',drawbounds=False)

        colors={}
        statenames=[]
        cmap = plt.cm.hot_r # use 'reversed hot' colormap
        vmin = 0; vmax = 450 # set range.
        norm = Normalize(vmin=vmin, vmax=vmax)

        for shapedict in m.states_info:
            statename = shapedict['NAME']
            # skip DC and Puerto Rico.
            if statename not in ['District of Columbia','Puerto Rico']:
                #pop = popdensity[statename]
                # calling colormap with value between 0 and 1 returns
                # rgba value.  Invert color range (hot colors are high
                # population), take sqrt root to spread out colors more.
                colors[statename] = cmap(3)
                pass
            statenames.append(statename)

        for nshape,seg in enumerate(m.states):
            # skip DC and Puerto Rico.
            if statenames[nshape] not in ['Puerto Rico', 'District of Columbia']:
                color = rgb2hex(colors[statenames[nshape]])
                poly = Polygon(seg,facecolor=color,edgecolor=color)
                ax.add_patch(poly)


        plt.axis('off')
        plt.axis("tight")
        plt.axis("image")

        AREA_1 = 0.005  # exclude small Hawaiian islands that are smaller than AREA_1
        AREA_2 = AREA_1 * 30.0  # exclude Alaskan islands that are smaller than AREA_2
        AK_SCALE = 0.19  # scale down Alaska to show as a map inset
        HI_OFFSET_X = -1900000  # X coordinate offset amount to move Hawaii "beneath" Texas
        HI_OFFSET_Y = 250000    # similar to above: Y offset for Hawaii
        AK_OFFSET_X = -250000   # X offset for Alaska (These four values are obtained
        AK_OFFSET_Y = -750000   # via manual trial and error, thus changing them is not recommended.)

        for nshape, shapedict in enumerate(m_.states_info):  # plot Alaska and Hawaii as map insets
            if shapedict['NAME'] in ['Alaska', 'Hawaii']:
                seg = m_.states[int(shapedict['SHAPENUM'] - 1)]
                if shapedict['NAME'] == 'Hawaii' and float(shapedict['AREA']) > AREA_1:
                    seg = [(x + HI_OFFSET_X, y + HI_OFFSET_Y) for x, y in seg]
                    color = rgb2hex(colors[statenames[nshape]])
                elif shapedict['NAME'] == 'Alaska' and float(shapedict['AREA']) > AREA_2:
                    seg = [(x*AK_SCALE + AK_OFFSET_X, y*AK_SCALE + AK_OFFSET_Y)\
                        for x, y in seg]
                    color = rgb2hex(colors[statenames[nshape]])
                poly = Polygon(seg, facecolor=color, edgecolor='gray', linewidth=.45)
                ax.add_patch(poly)

        light_gray = [0.8]*3  # define light gray color RGB
        x1,y1 = m_([-190,-183,-180,-180,-175,-171,-171],[29,29,26,26,26,22,20])
        x2,y2 = m_([-180,-180,-177],[26,23,20])  # these numbers are fine-tuned manually
        m_.plot(x1,y1,color=light_gray,linewidth=0.8)  # do not change them drastically
        m_.plot(x2,y2,color=light_gray,linewidth=0.8)

        #%% ---------   Show color bar  ---------------------------------------
        #ax_c = fig.add_axes([0.9, 0.1, 0.03, 0.8])
        #cb = ColorbarBase(ax_c,cmap=cmap,norm=norm,orientation='vertical',
        #                  label=r'[population per $\mathregular{km^2}$]')
        #ax = fig.gca()
        #ax.plot([1, 2, 4])

        plt.axis("off")
        ax.margins(x=0, y=0, tight=True)
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()

        size = canvas.get_width_height()
        surf = pygame.image.frombuffer (raw_data, size, "RGBA")

