import sys
import random
import json
import string
import csv
from decimal import Decimal
import time


def gen_random_decimal(i, d):
    """Generates random decimal based on input"""
    return Decimal("%d.%d" % (random.randrange(i + 1), random.randrange(1000,d + 1)))


def generate_a_column():
    """Generates values for column A in both files"""
    result_set = {}
    t1_bval = gen_random_decimal(9999, 9999)
    t2_acol = lambda a: str(a) + str(random.randint(1, 9999))
    t1_aval = float(t2_acol(t1_bval))
    result_set = {0: t1_aval, 1: t1_bval}
    return result_set



def generate_b_column():
    """Generates strings for column B in both files. 
    If result string is empty replaces it with null for second file"""
    result_string = "".join(
        random.sample(string.ascii_letters, k=random.randrange(20))
    )
    null_string = "null" if not result_string else result_string
    result_set = {0: result_string, 1: null_string}
    return result_set



def generate_c_column():
    """Generates simple jsons with pseudorandom element order without elements with empty values"""
    result_set = {}
    data = {}
    lists = ["a", "b", "c", "d", "e", "f"]
    n_samples = random.randint(1, 6)
    res = random.sample(lists, k=n_samples)
    data = {row: random.randint(1, 100) for row in res}
    keys = list(data.keys())
    random.shuffle(keys)
    rez = {key: data[key] for key in keys}

    result_set = {0: json.dumps(data), 1: json.dumps(rez)}
    return result_set



def generate_d_column():
    """Generates simple jsons in pseudorandom order with elements containing empty values"""
    lists = ["a", "b", "c", "d", "e", "f"]
    n_samples = random.randint(2, 6)
    res = random.sample(lists, k=n_samples)

    def get_value():
        rand = random.randint(-1, 10)
        values = {-1: "", 0: None}
        return values.get(rand, rand)
    
    data = {row: get_value() for row in res}

    keys = list(data.keys())
    random.shuffle(keys)
    rez = {key: data[key] for key in keys}

    result_set = {0: json.dumps(data), 1: json.dumps(rez)}
    return result_set

def generate_e_column():
    """Returns value from the list"""
    x = random.randint(1, 7)
    data = {
        1: "true",
        2: "false",
        3: "True",
        4: "False",
        5: "true",
        6: "FALSE",
        7: "null",
    }
    return data[x]


def writeFile(textWrap):
    tsv_writer = csv.writer(
        textWrap,
        delimiter="\t",
        lineterminator="\r\n",
        quotechar="'",
        quoting=csv.QUOTE_NONE
    )
    return tsv_writer

#Assumption: 1 file per hive table are  generated
def main(n_rows):
    """Creates two files with generated data"""
    file_a_name = "tableA.tsv"
    file_b_name = "tableB.tsv"
    with open(file_a_name, "w", newline="") as outA_file, open(
        file_b_name, "w", newline=""
    ) as outB_file:
        tsvA_writer = writeFile(outA_file)
        tsvB_writer = writeFile(outB_file)
        for row in range(n_rows):
            AVal = generate_a_column()
            BVal = generate_b_column()
            CVal = generate_c_column()
            DVal = generate_d_column()
            EVal = generate_e_column()
            tsvA_writer.writerow([AVal[0], BVal[0], CVal[0], DVal[0], EVal])
            tsvB_writer.writerow([AVal[1], BVal[1], CVal[1], DVal[1], EVal])


if __name__ == "__main__":
    #start_time = time.time()
    main(1000000)
    #elapsed = time.time() - start_time
