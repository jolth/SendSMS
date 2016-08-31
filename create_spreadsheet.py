#!/usr/bin/env python
# Copyright (c) 2016 Jorge Toro.
"""file csv parsing:
usage: create_spreadsheet template file output_file 

example: ./create_spreadsheet.py "\${name}, happy birthday" file.csv out.csv 
"""
from __future__ import print_function
import sys
import csv
from string import Template

#csv.register_dialect("comcel", delimiter='|')

def reader(f):
    """reader file csv.
    example: r = reader(file.csv); r.__next__()"""
    with open(f, r'rt') as f:
        field = csv.DictReader(f)
        for row in field:
            yield row


def temparsing(buffer, template):
    """template parsing"""
    print("Template [length: {1}]: {0}".format(template.template,
        len(template.template))) # debug
    try:
        for row in buffer:
            yield (row, template.substitute(row, 
                name=row['name'].split(' ')[0]))
    except KeyError as e:
        print("{0} key not existing into .csv".format(e))


def comcelwriter(f, buffer):
    with open(f, r'wt') as f:
        for k, d in buffer: 
            f.write("{0[phone]}|{1}\n".format(k, d))


if __name__ == "__main__":
    template = Template(sys.argv[1]) 
    reads = reader(sys.argv[2])
    
    b = temparsing(reads, template)
    comcelwriter(sys.argv[3], b)
