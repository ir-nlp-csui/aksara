#!/usr/bin/python3

def parse(rows):
    new_rows = []
    for row in rows:
        new_rows.append(row.split("\t"))

    return new_rows
