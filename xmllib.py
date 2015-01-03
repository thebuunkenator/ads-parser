import xml.etree.ElementTree as ET

def xml_value (record, parameter):
    """Retrieves a string value of the parameter"""
    if record.find(parameter) != None:
        value = record.find(parameter).text.encode('utf-8')
        #print parameter + ": "  + value
        return value
    else:
        #print parameter + ": not found."
        return ""


def xml_multiple_values (record, parameter):
    """Prints a multiple string value of the parameter array"""
    print parameter + 's:'
    for item in record.iter(parameter):
        print "\t" + item.text.encode('utf-8')
