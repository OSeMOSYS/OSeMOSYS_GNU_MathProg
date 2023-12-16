"""Translate TS naming to make it compatible with the new UI naming convention

This script renames the timeslices in the csv files (and actually any other items)
as defined in the tsnaming.csv file (see example in this folder).  This is needed
to import models into the new UI as the timeslices need to be named S11, S12, S21,
etc. to indicate day 1 of season 1 (S11), day 3 or season 6 (S63), etc.

Call this script with the following options:
1. Input data directory - set of csvs to adjust.
2. Output directory - where to put the converted csvs.

Script created 2023 by Taco Niet.  Apache-2.0 license.

"""

import os, sys, csv

def main(data_indirectory, data_outdirectory):
    with open("tsnaming.csv", "r") as tsitems:
        tslist = list(csv.reader(tsitems))
    for csv_name in os.listdir(data_indirectory):
        if csv_name.endswith('.csv'):
            text = open(os.path.join(data_indirectory, csv_name), "r")     
            for line in tslist:
                #print(csv_name)
                text = ''.join([i for i in text]).replace(line[0], line[1])
            x = open(os.path.join(data_outdirectory, csv_name),"w")
            x.writelines(text)
            x.close()
# end main


if __name__ == '__main__':
    if len(sys.argv) != 3:
        msg = "Usage: python {} <indir> <outdir>"
        print(msg.format(sys.argv[0]))
        sys.exit(1)
    else:
        data_indir = sys.argv[1]
        data_outdir = sys.argv[2]
        main(data_indir, data_outdir)