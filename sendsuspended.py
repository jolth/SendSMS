#!/usr/bin/env python
# Copyright (c) 2017 Jorge Toro.
"""send sms to the your suspended"""
from __future__ import print_function
import sys
import csv
import argparse

parser = argparse.ArgumentParser(
        description="Location the to vehicles suspended"
    )
parser.add_argument("-d", action="store", dest="dbname")
parser.add_argument("-c", action="store", dest="csvfile")

arg = parser.parse_args()


def csv_reader(csvfile):
    with open(csvfile, r'rt') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def db_reader(cursor):
    while True:
            plate = (yield)
            if plate:
                pass


if __name__ == "__main__":
    if arg.csvfile:
        for row in csv_reader(arg.csvfile):
            print(row['plate'])
