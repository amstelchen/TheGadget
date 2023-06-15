import os
import logging
import nltk

from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

from __version__ import PROGNAME
from utils import Data

text = '''
This is a sample text that contains the name Alex Smith who is one of the developers of this project.
You can also find the surname Jones here.
'''

def find_names(text):
    nltk_results = ne_chunk(pos_tag(word_tokenize(text)))
    for nltk_result in nltk_results:
        if type(nltk_result) == Tree:
            name = ''
            for nltk_result_leaf in nltk_result.leaves():
                name += nltk_result_leaf[0] + ' '
            print ('Type: ', nltk_result.label(), 'Name: ', name)

def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    
    loader = Data(os.path.join(os.path.dirname(__file__), 'resources', 'database', PROGNAME + ".db"))
    dates_data = loader.load_table_data("Dates", "ORDER BY event_date")
    people_data = loader.load_table_data("People")
    logging.debug(f"Loaded {len(dates_data)} dates, {len(people_data)} people.")

    # Generate the names
    #event_list =  []
    for event_name in dates_data:
        logging.info(f"Querying name: {event_name[2]}")
        result = find_names(event_name[3])

if __name__ == '__main__':
    main()
