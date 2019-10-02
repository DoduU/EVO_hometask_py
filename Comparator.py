import csv
from operator import itemgetter
from decimal import Decimal
import json
import math


def prepare_json(row):
    """Removes optional spaces for every item key.
    Removes empty or null elements.Sorts json"""
    ignored_values = set(["null", "", None])
    parsed_row = json.loads(row)
    parsed_row = {
        k.strip(): v for k, v in parsed_row.items() if v not in ignored_values
    }
    return sorted(parsed_row.items())


def null_handl(strg):
    """Null value handler"""
    return "" if strg == "null" else strg


def ds_grooming(ds):
    """Cleans every element based on requirements"""
    gr_list = list()
    for a_col, b_col, c_col, d_col, e_col in ds:
        gr_list.append(
            [
                (math.floor(Decimal(a_col) * 1000) / 1000),
                null_handl(b_col.lower()),
                prepare_json(c_col),
                prepare_json(d_col),
                e_col.lower().strip(),
            ]
        )
    return gr_list

#Assumption: Hive export contains just one file.
def sort_by(file_n, delim):
    """Reads and sorts input file"""
    with open(file_n) as f:
        r = csv.reader(f, delimiter=delim)
        r = sorted(ds_grooming(r), key=itemgetter(0, 1, 2, 3, 4))

    return r

#Assumption: Files contain the same number of unique records. Logic for handling duplicates is not implemented.
def zip_compare(zip_file):
    """Compare zipped elemets"""
    i = 0
    for line_a, line_b in zip_file:
        i += 1
        if not (line_a == line_b):
            return -1
    return i


def main(file1_name, file2_name):
    a_list = sort_by(file1_name, "\t")
    b_list = sort_by(file2_name, "\t")

    combained_ab = zip(a_list, b_list)
    rez = zip_compare(combained_ab)
    print("The files are identical. Total number of rows is: " + str(rez)) if rez != -1 else print("The files are not equal.")


if __name__ == "__main__":
    # start_time = time.time()
    file1_name = "tableA.tsv"
    file2_name = "tableB.tsv"
    main(file1_name, file2_name)
    # elapsed = time.time() - start_time
