import json
import os
import requests

"""This class defines static utility methods for working with files i/o with auto support for JSON"""

from datetime import date, datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def read_json(filename):
    """Read contents of file specified by 'filename' and return as parsed JSON"""
    with open(filename, 'r') as file_contents:
        return json.load(file_contents)

def write_json(filename, json_array, indent=0):
    """Write JSON object to file specified by 'filename'"""
    json_string = json.dumps(json_array, indent=indent, default=json_serial)
    write_file(filename, json_string)


def read_file(file_name):
    """Read contents of file specified by 'filename' and return as a string"""
    with open(file_name, 'r') as file_contents:
        return file_contents


def write_file(file_name, content):
    """Write String object to file specified by 'filename'"""
    f = open(file_name, "w")
    f.write(content)
    f.close()


def delete_file(filename):
    """Delete object specified by 'filename'"""
    os.remove(filename)


def download_file_from_url(url, filename):
    file = requests.get(url)
    open(filename, 'wb').write(file.content)