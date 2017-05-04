#!/usr/bin/env python
# Copyright (c) 2017 Jorge Toro.
# $ python sendsuspended.py -u postgres -d rastree -W qwerty -f suspendidos.csv
"""send sms to the your suspended"""
from __future__ import print_function
import sys
import csv
import argparse
import psycopg2

parser = argparse.ArgumentParser(
        description="Location the to vehicles suspended"
    )
parser.add_argument("-d", action="store", dest="dbname")
parser.add_argument("-u", action="store", dest="user")
parser.add_argument("-W", action="store", dest="password")
parser.add_argument("-f", action="store", dest="csvfile")
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
                cursor.execute("SELECT * FROM vehiculos WHERE placa='{0}';".format(plate.lower()))
                print(cursor.fetchone())


if __name__ == "__main__":
    connect = psycopg2.connect("dbname={0} user={1}\
            password={2}".format(arg.dbname, arg.user, arg.password))
    cursor = connect.cursor()

    reader = db_reader(cursor)
    reader.__next__()
    if arg.csvfile:
        print(arg.csvfile)
        for row in csv_reader(arg.csvfile):
            reader.send(row['plate'])

    connect.commit()
    cursor.close()
    connect.close()
