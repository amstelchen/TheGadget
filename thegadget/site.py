import os
import re
import io
import tempfile
import logging

from collections import OrderedDict
from os import listdir, linesep
from os.path import isfile, join, basename, splitext

import pygame
import pygame_gui

from pygame import Rect
from pygame.image import load
from pygame_gui.elements import UITextBox, UIWindow, UITextEntryLine, UILabel, UIButton, UIImage, UIProgressBar

from .utils import Data
import staticmaps
import cairosvg
import geopandas

resources_path = os.path.join(os.path.dirname(__file__), 'resources')

#context = staticmaps.Context()
#context.set_tile_provider(staticmaps.tile_provider_OSM)
#frankfurt = staticmaps.create_latlng(50.110644, 8.682092)
#context.add_object(staticmaps.Marker(frankfurt, color=staticmaps.GREEN, size=12))

# render non-anti-aliased png
#image = context.render_pillow(800, 500)
#image.save("frankfurt_area.pillow.png")

# render anti-aliased png (this only works if pycairo is installed)
#image = context.render_cairo(800, 500)
#image.write_to_png("frankfurt_area.cairo.png")

# render svg
#svg_image = context.render_svg(800, 500)
#with open("frankfurt_area.svg", "w", encoding="utf-8") as f:
#    svg_image.write(f, pretty=True)

class SiteWindow(UIWindow):
    def __init__(self, manager, title, pos: tuple, size: tuple, sitedata, buildings, zoom = 15):
        super().__init__(
            Rect(
                pos, size),  # (200, 50), (420, 520)),
            manager,
            window_display_title=title,
            object_id="#site_window")

        self.page_y_start_pos = 0

        tool_bar_top_margin = 2
        tool_bar_bottom_margin = 2
        """self.search_box = UITextEntryLine(
            Rect(
                (150, search_bar_top_margin),
                (230, 30)),
            manager=manager,
            container=self,
            parent_element=self)"""

        self.search_label = UILabel(
            Rect(
                (90, tool_bar_top_margin),
                (56, 30)),
            "Search:",
            manager=manager,
            container=self,
            parent_element=self,)

        self.home_button = UIButton(
            Rect(
                (20, tool_bar_top_margin),
                (29, 29)),
            '',
            manager=manager,
            container=self,
            parent_element=self,
            object_id='#home_button')

        self.remaining_window_size = (
            self.get_container().get_size()[0],
                (self.get_container().get_size()[1] -
                    (30 +
                        tool_bar_top_margin +
                        tool_bar_bottom_margin + 500)))

        self.page_y_start_pos = (
            tool_bar_top_margin +
            tool_bar_bottom_margin)

        #image_surface = load(os.path.join(resources_path, "techtree", "test_emoji.png"))

        img_dim = 128
        #self.page_y_start_pos += 100

        rem_width, rem_height = self.get_container().get_size()
        logging.debug(f"{rem_width = }, {rem_height = }")

        context = staticmaps.Context()
        context.set_tile_provider(staticmaps.tile_provider_OSM)

        # (22, 'Chalk River, Quebec, Canada', 46.050242, -77.361002, 918.22, 175.54, "...", None, 15)
        # lat, lon = 46.050242, -77.361002
        lat, lon = float(sitedata[2]), float(sitedata[3])
        logging.debug(f"{lat = }, {lon = }")

        # sitedata_coords = buildings
        """
        coords_polygon = [
            (46.0495029, -77.3626987),
            (46.049103, -77.3625964),
            (46.0492681, -77.3612548),
            (46.0496682, -77.3613571),
            (46.0495029, -77.3626987),
        ]
        coords_polygon = [(-77.3626987, 46.0495029), (-77.3625964, 46.049103), (-77.3612548, 46.0492681), (-77.3613571, 46.0496682), (-77.3626987, 46.0495029)]
        context.add_object(
            staticmaps.Area(
                [staticmaps.create_latlng(lat, lng) for lat, lng in coords_polygon],
                fill_color=staticmaps.parse_color("#00FF003F"),
                width=2,
                color=staticmaps.BLUE,
            )
        )
        """
        print(f"{buildings = }")
        # for coords_polygon in sitedata_coords:
        
        # irgendwo wird lat und lon vertauscht, darum unten auch getauscht:
        for building in buildings:
            coords_polygon = list(building)
            print(f"{coords_polygon = }")
            context.add_object(
                staticmaps.Area(
                    [staticmaps.create_latlng(lng, lat) for lat, lng in coords_polygon],
                    fill_color=staticmaps.parse_color("#00FF003F"),
                    width=2,
                    color=staticmaps.BLUE,
                )
            )
        
        context.set_zoom(zoom)
        #city = staticmaps.create_latlng(50.110644, 8.682092)
        city = staticmaps.create_latlng(lat, lon)

        context.add_object(staticmaps.Marker(city, color=staticmaps.GREEN, size=12))
        #context.add_object(staticmaps.)

        # render non-anti-aliased png
        #image = context.render_pillow(rem_width, rem_height)

        # render anti-aliased png (this only works if pycairo is installed)
        image = context.render_cairo(rem_width, rem_height)

        image.write_to_png("tmp1.png")

        png_data = io.BytesIO()
        with tempfile.TemporaryFile(mode="rb+") as fp:
            image.write_to_png(fp)
        #png_data = io.BytesIO(image)
        #png_data.read(image)
            png_io = io.BytesIO()
        
            #cairosvg.svg2png(png_data, write_to=fp)
            fp.seek(0)
            #png_surf = load(fp, "png")
        png_surf = load("tmp1.png")

        # render svg
        #svg_image = context.render_svg(800, 500)

        #svg_io = svg_image.tostring()
        #svg_io = io.BytesIO(initial_bytes=svg_image.get_xml())
        #png_io = io.BytesIO()
        #cairosvg.svg2png(bytestring=svg_io, write_to=png_io)
        #png_io.seek(0)
        #png_data = load(png_io, "png")

        self.map_display = UIImage(
            relative_rect=Rect(0, 0, rem_width, rem_height),
            image_surface=png_surf,
            manager=manager,
            container=self,
            parent_element=self,
            object_id='#site_image')

        self.info_box = UITextBox(
            f"Site name: {title} \n" \
            f"Location: {sitedata[2], sitedata[3]}\n" \
            f"Workers: {sitedata[7]}\n" \
            f"\n{sitedata[6]}",
            Rect(
                (self.get_container().get_size()[0] - 425, 25 + self.page_y_start_pos),
                (400, 250)),
            manager=manager,
            container=self.map_display.ui_container,
            parent_element=self.map_display)

        self.buy_button = UIButton(
            Rect(
                (self.get_container().get_size()[0] - 425, 25 + self.page_y_start_pos + 250),
                (48, 48)),
            '',
            manager=manager,
            container=self.map_display.ui_container,
            parent_element=self,
            object_id='#buy_button')

    def process_event(self, event):
        handled = super().process_event(event)

        if event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
            self.open_new_page(event.link_target)
            handled = True

        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == '#site_window.#home_button'):
            self.open_new_page('index')
            handled = True

        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == '#site_window.#buy_button'):
            # self.open_new_page('index')
            handled = True

        return handled

