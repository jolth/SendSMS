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

csv.register_dialect("comcel", delimiter='|')

template = Template(sys.argv[1]) 
print("Template:", template.template) # debug

def firstName(name):
    return name.split(' ')[0]

with open(sys.argv[2], r'rt') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = firstName(row["name"])
        t = template.substitute(name=name)
        print(t)
