import json
import os
import sys


#add project root to path so I can import a module from the wikidata folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
from wikidata.manual_data import FACTION_SHORT_NAMES

INFILE = 'db_dump/data/factions/factions-formatted.json'
OUTFILE = 'db_dump/data/factions/factions-final.json'

def add_shortname(faction):
    faction['labelAlternative'] = FACTION_SHORT_NAMES[faction['id']]
    return faction

with open(INFILE) as infile:
    data = json.load(infile)
    entries = [add_shortname(faction) for faction in data]
    entries.append({
        'type': 'faction', 
        'id': 'Q4316268', 
        'label': 'fraktionslos',
        'abstract': 'fraktionslose Abgeordnete'
    })
    with open(OUTFILE, 'w', encoding='utf8') as outfile:
        json.dump(entries, outfile, ensure_ascii=False)
        

