import os
import re
import logging
from collections import OrderedDict
from os import listdir, linesep
from os.path import isfile, join, basename, splitext

import pygame
import pygame_gui

from pygame import Rect
from pygame.image import load
from pygame_gui.elements import UITextBox, UIWindow, UITextEntryLine, UILabel, UIButton, UIImage, UIProgressBar

from .utils import Data, overlay_surfaces, garble_text

resources_path = os.path.join(os.path.dirname(__file__), 'resources')


class IntelWindow(UIWindow):
    def __init__(self, manager, title, pos: tuple, size: tuple, intel_info: list, intel_progress: dict):
        super().__init__(
            Rect(
                pos, size),  # (200, 50), (420, 520)),
            manager,
            window_display_title=title,
            object_id="#intel_window")

        overlay_surface = pygame.image.load(os.path.join(resources_path, "images", "arrested2.png")).convert_alpha()
        overlay_surface = pygame.transform.scale(overlay_surface, (200, 200))
        self.page_y_start_pos = 0

        search_bar_top_margin = 2
        search_bar_bottom_margin = 2
        self.search_box = UITextEntryLine(
            Rect(
                (150, search_bar_top_margin),
                (230, 30)),
            manager=manager,
            container=self,
            parent_element=self)

        self.search_label = UILabel(
            Rect(
                (90, search_bar_top_margin),
                (56, self.search_box.rect.height)),
            "Search:",
            manager=manager,
            container=self,
            parent_element=self,)

        self.home_button = UIButton(
            Rect(
                (20, search_bar_top_margin),
                (29, 29)),
            '',
            manager=manager,
            container=self,
            parent_element=self,
            object_id='#home_button')

        self.remaining_window_size = (
            self.get_container().get_size()[0],
                (self.get_container().get_size()[1] -
                    (self.search_box.rect.height +
                        search_bar_top_margin +
                        search_bar_bottom_margin + 500)))

        self.pages = {}
        page_path = os.path.join(resources_path, 'guiopedia')
        file_paths = [join(page_path, f) for f in listdir(page_path) if isfile(join(page_path, f))]
        for file_path in file_paths:
            with open(file_path, 'r') as page_file:
                file_id = splitext(basename(file_path))[0]
                file_data = ""
                for line in page_file:
                    line = line.rstrip(linesep).lstrip()
                    # kind of hacky way to add back spaces at the end of new lines that
                    # are removed by the pyCharm HTML
                    # editor. perhaps our HTML parser needs to handle this case
                    # (turning new lines into spaces
                    # but removing spaces at the start of rendered lines?)
                    if len(line) > 0:
                        if line[-1] != '>':
                            line += ' '
                        file_data += line
                self.pages[file_id] = file_data

        index_page = self.pages['intel']

        self.page_y_start_pos = (
            self.search_box.rect.height +
            search_bar_top_margin +
            search_bar_bottom_margin)

        self.page_display = UITextBox(
            index_page,
            Rect(
                (0, self.page_y_start_pos),
                self.remaining_window_size),
            manager=manager,
            container=self,
            parent_element=self)

        #image_surface = load(os.path.join(resources_path, "techtree", "test_emoji.png"))

        img_dim = 128
        #self.page_y_start_pos += 100

        self.rect_images = []
        img_person = "Klaus Fuchs"
        spy_iter = 0
        for _, intel_file in enumerate(intel_info):
            spy_iter = _
            intel_info[_] += (pygame.Rect(10 + (spy_iter) * 1.1 * img_dim + 10, self.page_y_start_pos + img_dim + 100, img_dim, img_dim),)
            intel_info[_] += (pygame.Rect(10 + (spy_iter) * 1.1 * img_dim, self.page_y_start_pos - 30 + img_dim * 3, img_dim + 10, img_dim // 2),)

            spy_id = intel_file[0]
            spy_name = intel_file[1]
            spy_portrait = intel_file[7]
            img_rect = intel_info[_][8]
            text_rect = intel_info[_][9]

            softened_image = pygame.transform.gaussian_blur(surface=spy_portrait, radius=100 - intel_progress.get(spy_id) + 1)
            logging.debug(f"{spy_name}: {100 - intel_progress.get(spy_id)}")

            spy_name = garble_text(spy_name, 1 - intel_progress.get(spy_id) / 100)

            button_enabled = True
            if intel_progress.get(spy_id) > 0:
                button_enabled = False

            button_status = "Investigate"
            if intel_progress.get(spy_id) > 0:
                button_status = "Investigating"
            if intel_progress.get(spy_id) == 100:
                softened_image = overlay_surfaces(softened_image, overlay_surface)
                button_status = "Arrested"

            UIImage(
                relative_rect=img_rect,
                image_surface=softened_image,  # was spy_portrait,
                manager=manager,
                container=self,
                parent_element=self,
                object_id='#spy_image')

            UILabel(
                relative_rect=text_rect,
                text=spy_name,
                manager=manager,
                container=self,
                parent_element=self,
                object_id='#spy_label')

            UIButton(
                relative_rect=Rect((text_rect.left, text_rect.top + 100), text_rect.size),
                text=button_status,
                manager=manager,
                container=self,
                parent_element=self,
                object_id=f'#spy_button_{spy_id}').is_enabled = button_enabled

            UIProgressBar(
                relative_rect=Rect((text_rect.left, text_rect.top + 200), text_rect.size),
                manager=manager,
                container=self,
                parent_element=self,
                object_id=f'#spy_progress_{spy_id}').set_current_progress(intel_progress.get(spy_id))

    def process_event(self, event):
        handled = super().process_event(event)

        if event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
            self.open_new_page(event.link_target)
            handled = True

        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == '#intel_window.#spy_button'):
            self.open_new_page('index')
            handled = True

#        if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
#                event.ui_element == self.search_box):
#            results = self.search_pages(event.text)
#            self.create_search_results_page(results)
#            self.open_new_page('results')
#            handled = True

        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == '#intel_window.#home_button'):
            self.open_new_page('index')
            handled = True

        return handled

