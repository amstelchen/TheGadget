import os
import requests
from bs4 import BeautifulSoup
#from game import Data
from __version__ import PROGNAME

def query_name(name):
    url = 'https://en.wikipedia.org/wiki/' + name

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None

    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        #result = soup.find('td', {'class': 'infobox-image'})
        result = soup.find('table', {'class': 'infobox'})

        if result is None:
            return "No results found for this name."
        else:
            image_url = "https:" + result.find("img").attrs.get("src")
            response = requests.get(image_url)
            with open(name + ".png", "wb") as f:
                f.write(response.content)

            return result.get_text(strip=True)
    except AttributeError:
        return None

def save_results_to_file(results):
    with open('name_results.txt', 'a+') as file:  # Change 'w' to 'a+' for appending
        for imei, result in results.items():
            file.write(f"Name: {imei}\nResult: {result}\n\n")

def main():
    #loader = Data(os.path.join(os.path.dirname(__file__), 'resources', 'database', PROGNAME + ".db"))
    #people_data = loader.load_table_data("People")

    name_list = ["J. Robert Oppenheimer",
"General Leslie R. Groves",
"Enrico Fermi",
"Niels Bohr",
"Richard Feynman",
"Edward Teller",
"Ernest Lawrence",
"Vannevar Bush",
"Klaus Fuchs",
"Arthur Compton",
"Carl David Anderson",
"Charles Lauritsen",
"Chien-Shiung Wu",
"Cyril Smith",
"David Bohm",
"Donald Hornig",
"Dorothy Hodgkin",
"Dorothy McKibbin",
"Edwin McMillan",
"Elizabeth Graves",
"Elizabeth Rona",
"Emilio Segrè",
"Eugene Wigner",
"Franklin Matthias",
"Frank Oppenheimer",
"George Gamow",
"George Kistiakowsky",
"George P. Thomson",
"Hans Bethe",
"Harold Urey",
"Hugh Bradner",
"Isidor Isaac Rabi",
"James Chadwick",
"James Franck",
"Joan Hinton",
"John Archibald Wheeler",
"John Manley",
"John von Neumann",
"Joseph Rotblat",
"Karl Cohen",
"Karl Compton",
"Katharine Way",
"Kenneth Bainbridge",
"Leona Woods",
"Leo Szilard",
"Leó Szilárd",
"Leslie Groves",
"Lise Meitner",
"Luis Alvarez",
"Maria Goeppert-Mayer",
"Melba Phillips",
"Norman Ramsey",
"Norris Bradbury",
"Otto Frisch",
"Philip Abelson",
"Philip Morrison",
"Richard Garwin",
"Richard Tolman",
"Robert Serber",
"Robert Wilson",
"Rudolf Peierls",
"Samuel Allison",
"Samuel Goudsmit",
"Seth Neddermeyer",
"Stanislaw Ulam",
"Thomas Farrell",
"Tsung-Dao Lee",
"Vera Rubin",
"William Sterling Parsons",]  # Generate the names

    results = {}

    for name in name_list:
        print(f"Querying name: {name}")
        result = query_name(name)
        if result is not None:
            results[name] = result

    save_results_to_file(results)

if __name__ == '__main__':
    main()
