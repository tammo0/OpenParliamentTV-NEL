import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
rootdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(rootdir)

import json
import wikidata.client as wikidata_client
from wikidata.queries import get_all_factions_of_germany

query = get_all_factions_of_germany()
results = wikidata_client.get(query)
print(results)
with open('factions.json', 'w') as outfile:
    json.dump(results, outfile)
