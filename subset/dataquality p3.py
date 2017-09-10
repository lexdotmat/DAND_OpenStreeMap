# Import re : Regular Expression
import re

from string import maketrans

osm_file = open("map.osm.xml", "r")

phone_number_format_CH = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)
phone_format = defaultdict(int)
# Audit Phone Numbers:

def audit_country:
    TODO(M): Audit country
    # tags:
    # files:

def phone_cleaning(phone_raw):
    '''
    :param phone_raw: a swiss phone number raw number in either format.
    :return: the phone number in the format +41 xx xxx xx xx
    '''
    phone_raw.replace(" ", "")
    return "+41"+ " " +phone_raw[-9:-7] + " " + phone_raw[-7:-4] + " " + phone_raw[-4:-2] + " " + phone_raw[-2:]

# mapping from https://www.tutorialspoint.com/python/string_maketrans.htm
# https://stackoverflow.com/questions/30141233/replacing-the-integers-in-a-string-with-xs-without-error-handling
mapping = maketrans("0123456789", "x"*10)

def audit_phone_type(Phone_number, Country = "CH"):

    # phone number format: +41 or 0 xx xxx xx xx
    # to finish

    if Country == "CH":
        m = Phone_number.translate(mapping)
        phone_format = m.group()

        phone_format[phone_type] += 1

        return phone_format


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

def is_phone_number(elem):
    return (elem.tag == "tag")
def audit():
    for event, elem in ET.iterparse(osm_file):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])    
    print_sorted_dict(street_types)    

if __name__ == '__main__':
    audit()