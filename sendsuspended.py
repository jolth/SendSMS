#!/usr/bin/env python
# Copyright (c) 2017 Jorge Toro.
# $ python sendsuspended.py -u postgres -d rastree -W qwerty -f suspendidos.csv
"""send sms to the your suspended"""
import sys
import csv
import argparse
import psycopg2
import datetime
import time

parser = argparse.ArgumentParser(
        description="Location the to vehicles suspended", add_help=True
    )
parser.add_argument("-d", action="store", dest="dbname", help="database name")
parser.add_argument("-u", action="store", dest="user", help="database user name")
parser.add_argument("-W", action="store", dest="password", help="database password")
parser.add_argument("-f", action="store", dest="csvfile", help="csv file")
parser.add_argument("-o", action="store", dest="outfile", help="out file",
        default="out.csv")
arg = parser.parse_args()

fnames = ("location", "date")
fieldnames = []
with open(arg.csvfile) as f:
    r = csv.DictReader(f)
    fieldnames.extend(r.fieldnames) #extract field names of the csv file
fieldnames.extend(fnames)


def csv_reader(csvfile):
    with open(csvfile, r'rt') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def db_reader(cursor):
    while True:
        row = (yield)
        cursor.execute("SELECT lp.ubicacion, lp.fecha FROM vehiculos v,\
                gps g, last_positions_gps lp WHERE g.id=lp.gps_id and\
                v.gps_id=g.id and v.placa='{0}';".format(row['plate'].lower()))
        row.update(zip(fnames, cursor.fetchone()))


def if_working(row):
    row['date'] = datetime.datetime(row['date'].year, row['date'].month, row['date'].day, row['date'].hour,
            row['date'].minute, row['date'].second)
    if row['date'] > (datetime.datetime.now() - datetime.timedelta(minutes=10)):
        row['working'] = 'Y'
    else:
        row['working'] = 'N'


def csv_writer(csvfile):
    with open(csvfile, r'wt') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        while True:
            row = (yield)
            print("write:", row)#debug
            time.sleep(0.1)#debug
            writer.writerow(row)


if __name__ == "__main__":
    connect = psycopg2.connect("dbname={0} user={1}\
            password={2}".format(arg.dbname, arg.user, arg.password))
    cursor = connect.cursor()

    reader = db_reader(cursor)
    reader.__next__()
    writer = csv_writer(arg.outfile)
    writer.__next__()
    if arg.csvfile:
        for row in csv_reader(arg.csvfile):
            if row['plate']:
                reader.send(row)
                if_working(row)
                writer.send(row)

    connect.commit()
    cursor.close()
    connect.close()
