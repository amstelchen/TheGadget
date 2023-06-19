import os
import time
import requests
import logging
from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim
from __version__ import PROGNAME
from utils import Data

api = Api()


def query_place(place):

    if place > 0: # place.isdigit():
        osm_id = place
    else:
        #way = api.query('way/5887599')
        nominatim = Nominatim()
        #areaId = nominatim.query(place).areaId()
        osm_id = nominatim.query(place)._json[0]['osm_id']
    if osm_id is None:
        return
    logging.debug(f"{osm_id = }")
    start = time.time()
    way = api.query(f'way/{osm_id}', onlyCached=False, shallow=False, history=False)
    logging.debug(f"{(time.time() - start) * 1000:3.4}ms")

    # Extracting the coordinates from the nodes
    coordinates = [(node.lon(), node.lat()) for node in way.nodes()]

    # Converting the coordinates to a WKT polygon
    wkt_polygon = 'POLYGON((' + ', '.join([f'{lon} {lat}' for lon, lat in coordinates]) + '))'

    #return way.tag("name"), way.nodes()
    return wkt_polygon

def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    
    loader = Data(os.path.join(os.path.dirname(__file__), 'resources', 'database', PROGNAME + ".db"))
    # places_data = loader.load_table_data("Places", "WHERE cx IS NOT NULL")
    buildings_data = loader.load_table_data("Buildings", "WHERE coords_polygon IS NULL")

    # places_data = [(1, 'Tower 270')]

    # Generate the names
    # for place in sorted([place[0] for place in buildings_data]): # places_data]):
    for place in sorted(buildings_data):
        logging.info(f"Querying place: {place[0]}")
        result = query_place(place[0])
        loader.update_table_data("Buildings", f"coords_polygon='{result}' WHERE building_id={place[0]}") #  name={place}")
        loader.update_table_data("Buildings", f"coords_text='{result}' WHERE building_id={place[0]}") #  name={place}")
        logging.info(result)
        # time.sleep(0.5)

if __name__ == '__main__':
    main()
