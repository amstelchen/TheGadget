import sys
import os
from pathlib import Path
from collections import deque
import pygame
from pygame.image import load
from pygame.locals import Color
import pygame_gui
import datetime
from datetime import date as dt
import logging
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex, Normalize
from matplotlib.patches import Polygon
from matplotlib.colorbar import ColorbarBase
import matplotlib.backends.backend_agg as agg
import sqlite3
import io

from .__version__ import PROGNAME, FULLNAME, VERSION, AUTHOR, DESC, __appname__, __description_short__, __studioname__, __controls__
from .utils import Data, SVG
from .stats import PlayerStats
from .gui import GUIWindow, ControlsWindow, StatusWindow, EventWindow, PersonWindow
from .tech import TechWindow
from pygame_gui.elements import UIImage, UILabel

from pygame_animatedgif import AnimatedGifSprite
import moviepy.editor

# workaround to include Cairo on Windows
os.environ['PATH'] += ";" + os.path.join(os.path.dirname(__file__), "resources", "dlls")
import cairosvg  # noqa: E402

resources_path = os.path.join(os.path.dirname(__file__), 'resources')

# video = moviepy.editor.VideoFileClip("/raid/Projekte/TheGadget/thegadget/resources/images/events/trinity_test.mpg")
video = moviepy.editor.VideoFileClip(os.path.join(resources_path, 'images/events/trinity_test.mpg'))

border_thin = 25
border_half = 50
border_wide = 100
status_window_width = 400
status_window_height = 150


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
            "fullscreen": 1,
            "show_fps": 0
        }

        # logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.basicConfig(format='%(levelname)s:%(asctime)s:%(filename)s:%(lineno)d:%(message)s', level=logging.DEBUG)

        self.loadDefaults()

        self.stats = PlayerStats()

        data_file = os.path.join(resources_path, 'database', PROGNAME + ".db")
        loader = Data(data_file)
        dates_data = loader.load_table_data("Dates")
        people_data = loader.load_table_data("People")
        places_data = loader.load_table_data("Places")
        tech_data = loader.load_table_data("Projects")
        logging.debug(f"Loaded {len(dates_data)} dates, {len(people_data)} people, {len(places_data)} places.")

        image_count1 = self.load_images(dates_data, 4, None, 420, 'events')
        image_count2 = self.load_images(people_data, 1, '.png', 200, None)
        logging.debug(f"Loaded images: {image_count1} dates, {image_count2} people.") # , {len(places_data)} places.")

        # Initialize Pygame, now handled in main()
        # pygame.init()

        self.audiostate = True
        self.fullScreenState = True

        # Set up the game window
        modes = pygame.display.list_modes()
        self.screen = pygame.display.set_mode(modes[0])
        pygame.display.toggle_fullscreen()
        pygame.display.set_caption(FULLNAME)
        self.screen = pygame.display.get_surface()
        self.window = self.screen

        logging.debug(f"Available modes: {[mode for mode in modes]}")
        logging.debug(f"Selected mode: {pygame.display.get_window_size()}")

        self.manager = pygame_gui.UIManager(self.screen.get_size(), os.path.join(resources_path, "themes/thegadget_theme.json"))
        self.manager.preload_fonts([{'name': 'fira_code', 'point_size': 24, 'style': 'bold'},
                                    {'name': 'fira_code', 'point_size': 24, 'style': 'bold_italic'},
                                    {'name': 'fira_code', 'point_size': 18, 'style': 'bold'},
                                    {'name': 'fira_code', 'point_size': 18, 'style': 'regular'},
                                    {'name': 'fira_code', 'point_size': 18, 'style': 'bold_italic'},
                                    {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
                                    ])

        self.research_progress = { 1: 100, 2: 80, 3: 40, 4: 25, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0 }

        # Game variables
        running = True
        logging.debug("Setting up clock...")
        self.fps_counter = None
        self.frame_timer = None
        self.clock = pygame.time.Clock()
        self.time_delta_stack = deque([], 2000)

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
        svg_file_div = os.path.join(os.path.dirname(__file__), "svgtest.svg")
        logging.debug("Images loaded.")

        #self.surface_div = pygame.image.load(svg_file_div)
        #self.surface_div = pygame.image.load(io.BytesIO(svg_string.encode()))
        #svg_io = io.BytesIO(svg_string.encode())
        #png_io = io.BytesIO()
        #with open(svg_file_div, "rb") as f:
        #    svg_cont = f.read()
        #    cairosvg.svg2png(file_obj=f, write_to=png_io)
        #    png_io.seek(0)
        #    self.surf = pygame.image.load(png_io, "png")
        #svg_io2 = io.BytesIO(svg_string.encode())
        #svg_io2 = bytes(svg_string.encode())
        #svg_io2.seek(0, io.SEEK_END)

        svg_io2 = svg_string.encode()
        png_io2 = io.BytesIO()
        cairosvg.svg2png(bytestring=svg_io2, write_to=png_io2)
        png_io2.seek(0)
        self.surface_div = pygame.image.load(png_io2, "png")

        #self.screen.fill(Color('#707070'))

        self.fps_counter = UILabel(manager=self.manager, relative_rect=pygame.Rect(self.screen.get_width() - 250, 20, 230, 44),
                                  text="", object_id='#fps_counter')  # was text="FPS: 0"

        self.frame_timer = UILabel(manager=self.manager, relative_rect=pygame.Rect(self.screen.get_width() - 250, 64, 230, 24),
                                   text="", object_id='#frame_timer')  # was text="Frame time: 0"

        self.intro_window = GUIWindow(manager=self.manager, title=FULLNAME, pos=(self.screen.get_width() - 500 - border_thin, border_thin), size=(500, 650), page="intro")

        self.controls_window = ControlsWindow(manager=self.manager, title="Controls", pos=(self.screen.get_width() - 500 - border_thin, 700), size=(500, 350), page="controls")

        self.ani_gif = AnimatedGifSprite((self.window.get_width() // 2 - 400, self.window.get_height() // 2 - 200), os.path.join(os.path.dirname(__file__), 'resources', 'images', 'events', 'TrinityDetonation1945GIF.gif'))
        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.ani_gif)

        bg_color = (0, 0, 0)

        # pygame.display.flip()

        # Fictional date
        start_date = datetime.date(1939, 8, 1)    # Szilard letter
        #start_date = datetime.date(1939, 9, 30)  # Leo Szilard
        #start_date = datetime.date(1945, 7, 14)  # Trinity test
        atest_date = datetime.date(1945, 7, 16)
        final_date = datetime.date(1947, 8, 15)
        #current_date = datetime.date(2023, 5, 24)
        
        self.current_date = start_date
        days_gone = 0

        self.status_window = StatusWindow(
            self.manager, "Current Date",
            (self.window.get_width() // 2 - status_window_width // 2 + border_thin, self.window.get_height() - status_window_height),
            (status_window_width, status_window_height),
            text=str(self.current_date))
        self.status_window.disable()

        # Game loop
        while running:
            #plt.show()

            time_delta = self.clock.tick(60) / 1000.0
            self.time_delta_stack.append(time_delta)
            if len(self.time_delta_stack) > 2000:
                self.time_delta_stack.popleft()

            # self.fps_counter.set_text(str(len(self.time_delta_stack)))

            # check for input
            # self.process_events()

            # respond to input
            self.manager.update(time_delta)

            if len(self.time_delta_stack) == 2000 and self.config["show_fps"] == '1':
                self.fps_counter.set_text(
                    f'FPS: {min(999.0, 1.0/max(sum(self.time_delta_stack)/2000.0, 0.0000001)):.2f}')
                self.frame_timer.set_text(f'Frame_time: {sum(self.time_delta_stack)/2000.0:.4f}')

            self.text_hist = ""

            #self.text = font_sml.render(f"Current Date: {current_date}", True, (0, 0, 0), Color("mediumaquamarine"))
            #self.text_rect = self.text.get_rect(center=(self.window.get_width() // 2 + border_thin, self.window.get_height() - 50))
            #text.fill(pygame.color.Color("mediumaquamarine"))

            self.updateDisplay()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # checking if keydown event happened or not
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        logging.debug("Key C has been pressed")
                        self.research_progress[5] += 20
                        #self.manager.process_events(event)
                        #self.manager.draw_ui(self.window)
                        #pygame.display.update()
                    
                    # checking if key "F" was pressed
                    if event.key == pygame.K_f:
                        logging.debug("Key F has been pressed")
                        if self.fullScreenState:
                            self.quitFullScreen(event)
                        else:
                            self.toggleFullScreen(event)
                        self.updateDisplay()
                    
                    # checking if key "A" was pressed
                    if event.key == pygame.K_r:
                        logging.debug("Key R has been pressed")
                        try:
                            # if not self.guiopedia_window.alive():
                            self.guiopedia_window.kill()
                        except AttributeError:
                            pass
                        finally:
                            self.research_window = TechWindow(
                                manager=self.manager, title="Research", 
                                pos=(border_wide, border_wide), 
                                size=(self.screen.get_width() - border_wide * 2, 800), 
                                techtree=tech_data, progress=self.research_progress)

                    # checking if key "W" was pressed
                    if event.key == pygame.K_w:
                        logging.debug("Key W has been pressed")
                        days_gone += 7
                        self.research_progress[6] += 10
                    
                    # checking if key "E" was pressed
                    if event.key == pygame.K_e:
                        logging.debug("Key e has been pressed")
                        days_gone += 31
                        self.research_progress[6] += 20

                    # checking if key "Q" was pressed
                    if event.key == pygame.K_q:
                        logging.debug("Key Q has been pressed")
                        running = False

                    # checking if key "S" was pressed
                    if event.key == pygame.K_s:
                        logging.debug("Key S has been pressed")
                        if sys.platform == 'linux':
                            save_file = os.path.join(str(Path('~').expanduser()), ".config", PROGNAME, "game_stats.json")
                        self.stats.save(save_file)
                        logging.debug("Game saved.")

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

                    if event.key == pygame.K_F1:
                        try:
                            # if not self.guiopedia_window.alive():
                            self.guiopedia_window.kill()
                        except AttributeError:
                            pass
                        finally:
                            self.guiopedia_window = GUIWindow(manager=self.manager, title=FULLNAME, pos=(self.screen.get_width() - 500 - border_thin, border_thin), size=(500, 800))

                    self.current_date = start_date + datetime.timedelta(days=days_gone)
                    logging.debug(f"{self.current_date = }")
                    #print(current_date.strftime("%Y-%m-%d"))
                        #print(type(dates_data))

                    for date_event in dates_data:
                        # logging.debug(date_event)
                        if datetime.datetime.combine(self.current_date, datetime.time(0, 0)) < datetime.datetime.strptime(date_event[1], "%Y-%m-%d"):
                            logging.debug(f"next date_event {date_event[1]}")
                            date_diff = (datetime.datetime.combine(self.current_date, datetime.time(0, 0)) - datetime.datetime.strptime(date_event[1], "%Y-%m-%d")).days * -1
                            logging.debug(f"{date_diff = }")
                            break

                    self.status_window.hide()

                    self.status_window = StatusWindow(
                        self.manager, "Current Date",
                        (self.window.get_width() // 2 - status_window_width // 2 + border_thin, self.window.get_height() - status_window_height),
                        (status_window_width, status_window_height),
                        text=str(self.current_date))
                    self.status_window.disable()

                    #self.manager.ui_group.remove(self.status_window)

                    for date_event in dates_data:
                        if self.current_date.strftime("%Y-%m-%d") == date_event[1]:
                            logging.debug("Date event found!")
                            self.text_hist = f"{date_event[1]}\n{date_event[2]}"
                            self.subtext = f"{date_event[3]}"
                            #eventImage = load(os.path.join(os.path.dirname(__file__), 'resources', 'images', 'events', date_event[4]))
                            #ratio = eventImage.get_height()/eventImage.get_width()
                            #eventImage = pygame.transform.scale(eventImage, (420, 420 * ratio))
                            #eventImage = eventImage.convert()

                            # self.intro_window.hide()

                            self.event_window = EventWindow(
                                self.manager, f"New event - {date_event[2]}", (self.window.get_width() // 2 - 400, self.window.get_height() // 2 - 200), (800, 400),
                            text=f"{date_event[1]}\n\n{date_event[3]}")
                            # image=eventImage)

                            if date_event[0] == 7:
                                self.manager.draw_ui(self.window)
                                pygame.display.update()
                                #for i in range(int(317)):
                                    #self.sprite_group.update(self.screen)
                                    #self.sprite_group.draw(self.screen)
                                    #self.manager.process_events(event)
                                    #self.clock.tick_busy_loop(33)
                                    #pygame.display.update()
                                #self.ani_gif.pause()
                                #self.ani_gif = None

                            eventImage = date_event[5]
                            self.image = UIImage(
                                relative_rect=pygame.Rect(
                                    (10, 10),
                                    (420, 420 // 1.3)),
                                image_surface=eventImage,
                                manager=self.manager,
                                container=self.event_window,
                                parent_element=self.event_window)

                    for people_event in people_data:
                        if self.current_date.strftime("%Y-%m-%d") == people_event[5]:
                            logging.debug("Person event found!")
                            self.text_hist = f"{people_event[5]}\n{people_event[1]} joined the Manhattan Project."
                            self.subtext = f"{people_event[4]}"
                            #charImage = load(os.path.join(os.path.dirname(__file__), 'resources', 'images', people_event[1] + '.png'))
                            #ratio = charImage.get_height()/charImage.get_width()
                            #charImage = pygame.transform.scale(charImage, (200, 200 * ratio))
                            #charImage = charImage.convert()

                            # self.intro_window.hide()

                            born = dt.fromisoformat(people_event[2])
                            born = dt.strftime(born, '%A, %d %B %Y')

                            self.person_window = PersonWindow(
                                self.manager, f"New person - {people_event[1]}", (self.window.get_width() // 2 - 300, self.window.get_height() // 2 - 200), (600, 400),
                                text=f"{people_event[1]} joined the Manhattan Project.\n\n{people_event[4]}<br><br>Born: {born},\n{people_event[3]}")
                                # image=charImage)

                            charImage = people_event[6]
                            self.image = UIImage(
                                relative_rect=pygame.Rect(
                                    (10, 10),
                                    (200, 200 * 1.3)),
                                image_surface=charImage,
                                manager=self.manager,
                                container=self.person_window,
                                parent_element=self.person_window)

                self.manager.process_events(event)

            # Update game logic
            # self.manager.update(time_delta)

            # Render the game
            self.manager.draw_ui(self.window)
            pygame.display.update()

            #surface = pygame.image.load('Manhattan_Project_US_Canada_Map_2.svg')
            #surface = pygame.transform.smoothscale(surface, (screen.get_width(), screen.get_height()))
            #screen.blit(surface, (0, 0))
            # Render SVG to Pygame surface using Pycairo
            #surface = cairosvg.surface.PNGSurface.from_file(svg_file)
            #with open(svg_file, "rb") as f:
            #    surface = cairosvg.surface.PNGSurface.convert(f)
            #    stream = io.BytesIO(surface.to_png())
            #    image = pygame.image.load(stream)

            # Control the frame rate
            #self.clock.tick(10)  # Cap the frame rate at 60 FPS

        # Quit the game
        logging.debug("Quitting.")
        pygame.quit()

    def load_images(self, dataset, load_column, use_ext: str = '', image_width = None, subfolder = ''):
        if use_ext is None:
            use_ext = ''
        if subfolder is None:
            subfolder = ''
        image_path = os.path.join(os.path.dirname(__file__), 'resources', 'images', str(subfolder))

        image_count = 0
        for _, row in enumerate(dataset):
            if row[load_column] is None:
                dataset[_] += (None,)
                continue
            if os.path.isfile(os.path.join(image_path, row[load_column]) + str(use_ext)):
                image = load(os.path.join(image_path, row[load_column]) + str(use_ext))
                ratio = image.get_height() / image.get_width()
                image = pygame.transform.scale(image, (image_width, image_width * ratio))
                image = image.convert()
                dataset[_] += (image,)
                image_count += 1

        return image_count
            #else:
             #   dataset[_] += (None,)

    def updateDisplay(self):
        self.screen.fill((255,255,255))
        #self.screen.fill(pygame.color.Color("mediumaquamarine"))

        # Display the fictional date
        #self.window.blit(self.text, self.text_rect)

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
                self.config = {}
                for configLine in configFile.readlines():
                    name, value = configLine.strip().split(" = ")
                    self.config[name] = value
                logging.debug(f"Settings loaded: {self.config}")
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

