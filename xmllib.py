import xml.etree.ElementTree as ET

namespace = "{http://ads.harvard.edu/schema/abs/1.1/abstracts}"

def xml_value (record, parameter):
    if record.find(parameter) != None:
        value = record.find(parameter).text.encode('utf-8')
        print parameter + ": "  + value
        return value
    else:
        print parameter + ": not found."
        return ""



def xml_multiple_values (record, parameter):
    print parameter + 's:'
    for item in record.iter(parameter):
        print "\t" + item.text.encode('utf-8')
