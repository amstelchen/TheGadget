import sqlite3


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

