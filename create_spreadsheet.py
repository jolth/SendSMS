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

def temParsing(buffer, template):
    """template parsing"""
    print("Template:", template.template) # debug
    try:
        for row in buffer:
            yield template.substitute(row)
    except KeyError as e:
        print("{0} key not existing into .csv".format(e))


if __name__ == "__main__":
    template = Template(sys.argv[1]) 

    #buffer = (r.__next__() for r in reader(sys.argv[2]))
    #for b in buffer:print(b)
    #for m in temParsing(buffer, template): print(m) # debug

    #debug
    #for row in reader(sys.argv[2]):
    #    if row["name"]: print(row, end='\n\n')

    reads = reader(sys.argv[2])
    #debug
    #try:
    #    print(reads.__next__(), end='\n\n')
    #    print(reads.__next__(), end='\n\n')
    #    print(reads.__next__(), end='\n\n')
    #    print(reads.__next__(), end='\n\n')
    #    print(reads.__next__(), end='\n\n')
    #    print(reads.__next__(), end='\n\n')
    #except StopIteration:
    #    print("Stop Iteration")

    #for r in reads:
    #    print(r,end='\n\n')

    t = temParsing(reads, template)
    #t = temParsing(reads, template)
    for r in t:
       print(r)
