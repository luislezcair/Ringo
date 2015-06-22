#!/usr/bin/env python

import sys
import os.path

# This is a tiny script to help you creating a CSV file from a face
# database with a similar hierarchie:
#
#  philipp@mango:~/facerec/data/at$ tree
#  .
#  |-- README
#  |-- s1
#  |   |-- 1.pgm
#  |   |-- ...
#  |   |-- 10.pgm
#  |-- s2
#  |   |-- 1.pgm
#  |   |-- ...
#  |   |-- 10.pgm
#  ...
#  |-- s40
#  |   |-- 1.pgm
#  |   |-- ...
#  |   |-- 10.pgm
#

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "usage: create_csv <base_path>"
        sys.exit(1)

    BASE_PATH = sys.argv[1]
    SEPARATOR = ";"

    label = 0
    for dirname, dirnames, filenames in os.walk(BASE_PATH):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)

            with open("%s/info.txt" % subject_path) as f:
                full_name = f.read().split(":")[1].strip()

            for filename in os.listdir(subject_path):
                if filename == "info.txt":
                    continue
                abs_path = "%s/%s" % (subject_path, filename)
                print("%s%s%d%s%s" % (abs_path, SEPARATOR, label, SEPARATOR, full_name))
            label += 1
