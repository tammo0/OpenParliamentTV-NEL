import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import helpers

INFILE = 'data/01_raw/parties/parties.json'
OUTFILE = 'data/02_formatted/parties.json'

def reformat(obj):
    flat = {key : value['value'] for (key, value) in obj.items()}
    id = flat.pop('ppg').split('/')[-1]
    label = flat.pop('ppgLabel')
    new = {
        'type': 'party', 
        'id': id, 
        'label': label,
        'socialMediaIDs': helpers.group_socials(flat),
        **flat
    }
    return new

# map over the entries and reformat each of them (reformatting means changing property names or grouping properties)
with open(INFILE) as infile:
    data = json.load(infile)
    entries = [reformat(entry) for entry in data['results']['bindings']]
    helpers.check_for_dups(entries)
    with open(OUTFILE, 'w', encoding="utf8") as outfile:
        json.dump(entries, outfile, ensure_ascii=False)

