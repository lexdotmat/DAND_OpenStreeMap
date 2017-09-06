# Import re : Regular Expression
import re

osm_file = open("map.osm.xml", "r")

phone_number_format_CH = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)

# Audit Phone Numbers:

def audit_country:
    TODO(M): Audit country
    # tags:
    # files:

def phone_cleaning(phone_raw):
    phone_raw.replace(" ", "")
    return "+41"+ " " +phone_raw[-9:-7] + " " + phone_raw[-7:-4] + " " + phone_raw[-4:-2] + " " + phone_raw[-2:]

def audit_street_type(Phone_number, Country):
    # phone number format: +41 or 0 xx xxx xx xx
    # to finish
    if Country == "CH":
        m = phone_number_format_CH.search(Phone_number)
    if m:
        street_type = m.group()

        street_types[street_type] += 1

# Audit_Street_type

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()

        street_types[street_type] += 1

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 

def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def audit():
    for event, elem in ET.iterparse(osm_file):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])    
    print_sorted_dict(street_types)    

if __name__ == '__main__':
    audit()