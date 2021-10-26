import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import helpers


INFILE_DE = 'db_dump/data/mdbs/mdbs-rawqueryresults_DE.json'
OUTFILE_DE = 'db_dump/data/mdbs/mdbs-formatted_DE.json'

INFILE_DE_BB = 'db_dump/data/mdbs/mdbs-rawqueryresults_DE-BB.json'
OUTFILE_DE_BB = 'db_dump/data/mdbs/mdbs-formatted_DE-BB.json'

def reformat(obj):
    flat = {key : value['value'] for (key, value) in obj.items()}
    id = flat.pop('mdb').split('/')[-1]
    label = flat.pop('mdbLabel')
    birthDate = None
    if 'dateOfBirth' in flat:
        birthDate = flat.pop('dateOfBirth', None).replace('T00:00:00Z', '')

    partyID = flat.pop('party', '').split('/')[-1]
    factionID = flat.pop('faction', '').split('/')[-1]
    new = {
        'type': 'memberOfParliament', 
        'id': id, 
        'label': label, 
        'birthDate': birthDate,
        'partyID': partyID if len(partyID)>0 else None,
        'factionID': factionID if len(factionID)>0 else None,
        'socialMediaIDs': helpers.group_socials(flat),
        'additionalInformation': helpers.group_additional_information(flat),
        **flat
    }
    return new

def process_file(infile_path, outfile_path):
    # map over the entries and reformat each of them (reformatting means changing property names or grouping properties)
    with open(infile_path) as infile:
        data = json.load(infile)
        entries = [reformat(entry) for entry in data['results']['bindings']]
        for e in entries:
            print(json.dumps(e, indent=4, sort_keys=True))
        with open(outfile_path, 'w', encoding='utf8') as outfile:
            json.dump(entries, outfile, ensure_ascii=False)


process_file(INFILE_DE, OUTFILE_DE)
process_file(INFILE_DE_BB, OUTFILE_DE_BB)