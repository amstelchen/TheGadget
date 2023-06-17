import os
import time
import requests
import logging
from bs4 import BeautifulSoup
#from game import Data
from __version__ import PROGNAME
from utils import Data

headers = {
    'User-Agent': 'ImageScrapingBot/0.1.0 (amstelchen@gmx.at) bot',
    'Accept-Encoding': 'gzip'
}
api_headers = {
    'Accept-Encoding': 'gzip',
    'Accept': 'application/json; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/Media/1.3.1"'
}

s = requests.Session()
s.headers.update(headers)

def query_name(name):

    url = 'https://en.wikipedia.org/api/rest_v1/page/summary/' + name.replace(' ', '_')
    try:
        response = requests.get(url, api_headers)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as err:
        logging.error(f"An error occurred: {err}")
        return None

    try:
        result = response.json()
        if result is None:
            return "No results found for this name."
        else:
            logging.debug(result['extract'])
            summary = result['extract']
            updater = Data(os.path.join(os.path.dirname(__file__), 'resources', 'database', PROGNAME + ".db"))
            updater.update_table_data("People", "description = '" + result['extract'].replace("\'", "''") + "' WHERE name = '" + name + "'")

    except (AttributeError, IndexError):
        return None

    #if os.path.isfile(os.path.join(os.path.dirname(__file__), 'resources', 'images', name + ".png")):
        logging.info(f"File {name + '.png'} already exists.")
    #    return None

    # url = 'https://en.wikipedia.org/wiki/' + name
    url = 'https://en.wikipedia.org/api/rest_v1/page/media-list/' + name.replace(' ', '_')

    try:
        response = requests.get(url, api_headers)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as err:
        logging.error(f"An error occurred: {err}")
        return None

    try:
        #soup = BeautifulSoup(response.text, 'html.parser')

        #result = soup.find('td', {'class': 'infobox-image'})
        #result = soup.find('table', {'class': 'infobox'})
        result = response.json()

        if result is None:
            return "No results found for this name."
        else:
            #image_url = "https:" + result.find("img").attrs.get("src")
            image_url = 'https:' + result['items'][0]['srcset'][0]['src']
            image_title = '' + result['items'][0]['title']
            response = s.get(image_url) # , headers)
            logging.debug(f"{response.status_code} {response.reason}")
            with open(os.path.join(os.path.dirname(__file__), 'resources', 'images', name + ".png"), "wb") as f:
                f.write(response.content)
            logging.debug(f"{len(response.content)} bytes written")

            # return summary # result.get_text(strip=True)
    except (AttributeError, IndexError):
        return None

    url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&iiextmetadatafilter=LicenseShortName&iiprop=extmetadata|url&prop=imageinfo&titles=' + image_title

    try:
        response = requests.get(url, api_headers)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as err:
        logging.error(f"An error occurred: {err}")
        return None

    try:
        result = response.json()
        if result is None:
            return "No results found for this name."
        else:
            logging.info(result['query']['pages']['-1']['imageinfo'][0]['extmetadata']['LicenseShortName']['value'])
    except (AttributeError, IndexError, KeyError):
        return None

def save_results_to_file(results):
    with open('name_results.log', 'w') as file:  # Change 'w' to 'a+' for appending
        for name, result in results.items():
            file.write(f"Name: {name}\nResult: {result}\n\n")

def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    
    loader = Data(os.path.join(os.path.dirname(__file__), 'resources', 'database', PROGNAME + ".db"))
    # people_data = loader.load_table_data("People", "WHERE description IS NULL")
    # for testing
    people_data = loader.load_table_data("People", "WHERE join_date IS NULL")

    # Generate the names
    name_list =  []
    for person_name in people_data:
        name_list.append(person_name[1])

    results = {}

    for name in sorted(name_list):
        logging.info(f"Querying name: {name}")
        result = query_name(name)
        if result is not None:
            results[name] = result
        # time.sleep(0.5)

    save_results_to_file(results)

if __name__ == '__main__':
    main()
