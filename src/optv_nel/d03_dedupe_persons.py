import os
import json
import ast
import datetime

#Deduce the PARLIAMENTS from the filenames in the /persons folder
INPUT_DIR = 'data/02_formatted/persons/'
OUTPUT_DIR = 'data/03_deduped/persons/'
INPUT_FILES = [f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, f))]
PARLIAMENTS = [f.split('.json')[0].split('formatted_')[-1] for f in INPUT_FILES]
print(PARLIAMENTS)

faction_keywords = ['factionID', 'factionStartTime', 'factionEndTime']
keywords_to_remove_from_final_output = ['factionStartTime', 'factionEndTime']

def clean_up(entry):
    for keyword in keywords_to_remove_from_final_output:
        if keyword in entry:
            del entry[keyword]
    return entry

def resolve_factions(entries):
    print("///Resolve factions for", entries[0]['id'])
    if len(entries)==1:
        return entries[0]['factionID']
    else:
        entries_with_faction_id = [entry for entry in entries if entry['factionID'] is not None]
        if(len(entries_with_faction_id)==0): #Case: empty list
            return None
        if(len(entries_with_faction_id)==1): #Case: There is just one option
            return entries_with_faction_id[0]['factionID']
        if(len(set([e['factionID'] for e in entries_with_faction_id]))) == 1: #Case: All faction ids are identical
            return entries_with_faction_id[0]['factionID']
        #Situation: We have multiple factions and need to decide which is the most actual one
        #Intuition 1: We take the one that has no end time (assuming it means that this faction is the recent one)
        no_endtime = [entry for entry in entries_with_faction_id if 'factionEndTime' not in entry]
        if len(no_endtime)>0:
            return no_endtime[0]['factionID']
        #Fallback: If there is no faction with missing end time, we sort the factions by start time and take the newest one
        print(entries_with_faction_id)
        newest_start_date = sorted(entries_with_faction_id, key=lambda x: datetime.datetime.strptime(x['factionStartTime'].replace('T00:00:00Z', ''), '%Y-%m-%d'), reverse=True)
        return newest_start_date[0]['factionID']

def remove_dups_from_list(thelist):
    if all(type(el) is dict for el in thelist):
        #we can't apply the set function to objects, lets convert them to string first
        strings = [str for str in set([str(el) for el in thelist])]
        return [ast.literal_eval(str) for str in strings]
    elif all(isinstance(el, list) for el in thelist):
        #we can't apply the set function to lists, lets convert them to string first
        strings = [str for str in set([str(el) for el in thelist])]
        return [ast.literal_eval(str) for str in strings]
    else:
        return [el for el in set(thelist)]

def get_all_keys(list_of_objects):
    keys = []
    for obj in list_of_objects:
        keys.extend(obj.keys())
    return set(keys)

def merge_dicts_additively(dicts):
    if(len(dicts)==1):
        print("/// No duplicate entries detected. Continue with next ID")
        return clean_up(dicts[0])
    print("/// Number of duplicates detected: ", len(dicts))
    result = {}
    for key in get_all_keys(dicts):
        if key in faction_keywords: #we'll deal with the factions later...
            continue
        result[key] = []
        for dic in dicts:
            try:
                result[key].append(dic[key])
            except: #...exception: Key is not present
                pass
        result[key] =  remove_dups_from_list(result[key])
        #Remove value None only if there are other values present
        if(len(result[key])>1):
            try: 
                result[key].remove(None) 
            except:
                pass
        #Remove lists with only 1 element
        if(len(result[key])==1):
            result[key] = result[key][0]
    result['factionID'] = resolve_factions(dicts)
    return result


def group_records_by_ids(data):
    groups = []
    for id in set([d['id'] for d in data]):
        entries = [d for d in data if d['id'] == id]
        groups.append(entries)
    return groups

def get_id(item):
    key = int(item['id'][1:]) #remove the Q from the ID
    return key

def process_file(infile_path, outfile_path):
    with open(infile_path) as infile:
        data = json.load(infile)
        cleaned = []
        groups = group_records_by_ids(data)
        for g in groups:
            print("")
            print("/// Currently handling", g[0]['id'], g[0]['label'])
            merged = merge_dicts_additively(g)
            cleaned.append(merged)
        cleaned.sort(key=get_id, reverse=True)
        with open(outfile_path, 'w', encoding='utf8') as outfile:
            json.dump(cleaned, outfile, ensure_ascii=False)

for PARLIAMENT in PARLIAMENTS:
    infile = INPUT_DIR + PARLIAMENT+'.json'
    outfile = OUTPUT_DIR + PARLIAMENT+'.json'
    process_file(infile, outfile)