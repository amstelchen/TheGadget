import os
import re
from collections import OrderedDict
from os import listdir, linesep
from os.path import isfile, join, basename, splitext

import pygame
import pygame_gui

from pygame import Rect
from pygame_gui.elements import UITextBox, UIWindow, UITextEntryLine, UILabel, UIButton, UIImage

resources_path = os.path.join(os.path.dirname(__file__), 'resources')


class StatusWindow(UIWindow):
    def __init__(self, manager, title, pos: tuple, size: tuple, text: str):
        super().__init__(
            Rect(
                pos, size),  # (200, 50), (420, 520)),
            manager,
            window_display_title=title,
            object_id="#status_window")

        self.remaining_window_size = (
            self.get_container().get_size()[0],
                (self.get_container().get_size()[1]))

        self.page_y_start_pos = 0

        self.page_display = UILabel(
            text=text,
            relative_rect=Rect(
                (0, self.page_y_start_pos),
                self.remaining_window_size),
            manager=manager,
            container=self,
            parent_element=self)

    def process_event(self, event):
        handled = super().process_event(event)

        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == '#guiopedia_window.#home_button'):
            self.open_new_page('index')
            handled = True
        return handled


class EventWindow(UIWindow):
    def __init__(self, manager, title, pos: tuple, size: tuple, text: str):
        super().__init__(
            Rect(
                pos, size),  # (200, 50), (420, 520)),
            manager,
            window_display_title=title,
            object_id="#status_window")

        self.remaining_window_size = (
            self.get_container().get_size()[0],
                (self.get_container().get_size()[1]))

        self.page_y_start_pos = 0

        self.page_display = UITextBox(
            text,
            relative_rect=Rect(
                (0, self.page_y_start_pos),
                self.remaining_window_size),
            manager=manager,
            container=self,
            parent_element=self)

    def process_event(self, event):
        handled = super().process_event(event)

        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == '#event_window.#home_button'):
            self.open_new_page('index')
            handled = True
        return handled


class PersonWindow(UIWindow):
    def __init__(self, manager, title, pos: tuple, size: tuple, text: str, image: pygame.surface.Surface):
        super().__init__(
            Rect(
                pos, size),  # (200, 50), (420, 520)),
            manager,
            window_display_title=title,
            object_id="#status_window")

        self.remaining_window_size = (
            self.get_container().get_size()[0] - 220,
                (self.get_container().get_size()[1]))

        self.page_y_start_pos = 0

        self.page_display = UITextBox(
            text,
            relative_rect=Rect(
                (220, self.page_y_start_pos),
                self.remaining_window_size),
            manager=manager,
            container=self,
            parent_element=self)

        """self.image = UIImage(
            relative_rect=Rect(
                (0, self.page_y_start_pos),
                self.remaining_window_size),
            image_surface=image,
            manager=manager,
            container=self,
            parent_element=self)"""

    def process_event(self, event):
        handled = super().process_event(event)

        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == '#event_window.#home_button'):
            self.open_new_page('index')
            handled = True
        return handled


class ControlsWindow(UIWindow):
    def __init__(self, manager, title, pos: tuple, size: tuple, page = None):
        super().__init__(
            Rect(
                pos, size),  # (200, 50), (420, 520)),
            manager,
            window_display_title=title,
            object_id="#controls_window")

        self.remaining_window_size = (
            self.get_container().get_size()[0],
                (self.get_container().get_size()[1]))

        self.page_y_start_pos = 0

        file_path = os.path.join(resources_path, 'guiopedia', 'controls.html')
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
            #self.pages[file_id] = file_data

        #index_page = "controls"

        self.page_display = UITextBox(
            file_data,
            Rect(
                (0, self.page_y_start_pos),
                self.remaining_window_size),
            manager=manager,
            container=self,
            parent_element=self)


class GUIWindow(UIWindow):
    def __init__(self, manager, title, pos: tuple, size: tuple, page = None):
        super().__init__(
            Rect(
                pos, size),  # (200, 50), (420, 520)),
            manager,
            window_display_title=title,
            object_id="#guiopedia_window")

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
                        search_bar_bottom_margin)))

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

        if page is None:
            index_page = self.pages['index']
        else:
            index_page = self.pages.get(page)

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

    def process_event(self, event):
        handled = super().process_event(event)

        if event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
            self.open_new_page(event.link_target)
            handled = True

        if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_element == self.search_box):
            results = self.search_pages(event.text)
            self.create_search_results_page(results)
            self.open_new_page('results')
            handled = True

        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == '#guiopedia_window.#home_button'):
            self.open_new_page('index')
            handled = True

        return handled

    def search_pages(self, search_string: str):
        results = {}
        words = search_string.split()

        for page in self.pages.keys():
            total_occurances_of_search_words = 0
            for word in words:
                word_occurances = self.search_text_for_occurrences_of_word(word, self.pages[page])
                total_occurances_of_search_words += word_occurances
            if total_occurances_of_search_words > 0:
                results[page] = total_occurances_of_search_words

        sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
        return OrderedDict(sorted_results)

    @staticmethod
    def search_text_for_occurrences_of_word(word_to_search_for: str, text_to_search: str) -> int:
        return sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word_to_search_for),
                                          text_to_search,
                                          flags=re.IGNORECASE))

    def open_new_page(self, page_link: str):
        self.page_display.kill()
        self.page_display = None
        if page_link in self.pages:
            text = self.pages[page_link]

            self.page_display = UITextBox(
                text,
                Rect(
                    (0, self.page_y_start_pos),
                    self.remaining_window_size),
                manager=self.ui_manager,
                container=self,
                parent_element=self)

    def create_search_results_page(self, results):
        results_text = '<font size=5>Search results</font>'
        if len(results) == 0:
            results_text += '<br><br> No Results Found.'
        else:
            results_text += '<br><br>' + str(len(results)) + ' results found:'
            for result in results.keys():
                results_text += '<br><br> - <a href=\"' + result + '\">' + result + '</a>'

        self.pages['results'] = results_text
