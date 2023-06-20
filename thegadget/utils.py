import sqlite3
import random
import pygame

def garble_text(text, percentage):
    garbled_text = ""
    for char in text:
        if char.isspace():  # Preserve whitespace
            garbled_text += char
        elif random.random() < percentage:
            garbled_text += random.choice('abcdefghijklmnopqrstuvwxyz')
        else:
            garbled_text += char
    return garbled_text

"""Example usage:
original_text = "This is a test sentence."
garbled_percentage = 0.2  # 20% garbling

garbled_text = garble_text(original_text, garbled_percentage)
print(garbled_text)
"""

def overlay_surfaces(background_surface, overlay_surface):
    # Create a new surface with the same size as the background surface
    merged_surface = pygame.Surface(background_surface.get_size(), pygame.SRCALPHA)

    # Calculate the coordinates to center the overlay surface on the background surface
    overlay_x = (background_surface.get_width() - overlay_surface.get_width()) // 2
    overlay_y = (background_surface.get_height() - overlay_surface.get_height()) // 2

    # Blit the background surface onto the merged surface
    merged_surface.blit(background_surface, (0, 0))

    # Blit the overlay surface onto the merged surface at the calculated coordinates
    merged_surface.blit(overlay_surface, (overlay_x, overlay_y))

    return merged_surface


class Data():
    def __init__(self, db_file):
        self.db_file = db_file

    def load_table_data(self, table_name, extra_sql = None):
        conn = sqlite3.connect(self.db_file)
        conn.enable_load_extension(True)
        conn.load_extension("mod_spatialite")
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name} {extra_sql}")
        data = cursor.fetchall()

        conn.close()

        return data

    def update_table_data(self, table_name, extra_sql = None):
        conn = sqlite3.connect(self.db_file)
        conn.enable_load_extension(True)
        conn.load_extension("mod_spatialite")
        cursor = conn.cursor()

        cursor.execute(f"UPDATE {table_name} SET {extra_sql}")
        #data = cursor.fetchall()
        conn.commit()

        conn.close()

        return cursor.lastrowid


class SVG():
    def __init__(self, places):
        self.places = places

    def create_markup(self):
        markup = """<svg viewBox="0 0 1212 769.85" xmlns="http://www.w3.org/2000/svg">
    <style>
        .small {
            font: bold 16px sans-serif;
            dominant-baseline: central;
        }
    </style>
"""
        for place in self.places:
            if place[4] is not None:
                place_name = place[1]
                cx = place[4]
                cy = place[5]
                markup += f'<text x="{ cx }" y="{ cy }" dx="25" class="small">{place[1]}</text>'
        return markup + "</svg>"

