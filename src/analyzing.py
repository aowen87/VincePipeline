__author__ = 'xixi'
'''
Created on Apr 24, 2016
Moldified on Mat 6, 2016
The first in a sequence of functions designed
to pipeline Mike Roundtree's BS-seq protocol.
Generated statistics for 5mC level, CHH, CG, CHG files.
@author: alister, xi
'''
import os
import sys
import argparse
import glob
from collections import defaultdict


def stepAnalyzing(file_dir, result_dir):

    if os.path.isdir(result_dir):
        print("\n{} already exists...".format(result_dir))
        cont = input("\nUsing this directory may result in current files being replaced. Would you like to continue? (y/n)")
        if cont != 'y':
            sys.exit("\nEXITING\n")
    else:
        os.system('mkdir {}'.format(result_dir))

    mCfiles = [file for file in glob.glob('./{}/*.txt'.format(file_dir))]
    mCfiles.sort()
    file_len = len(mCfiles)
    if file_len%2!=0:
        file_len-=1

    for i in range(0, file_len, 2):
        forw = mCfiles[i]
        rev = mCfiles[i+1]

        txt = ".txt"
        merge = result_dir+rev.replace("rev", "merge")+txt
        sort = result_dir+rev.replace("rev", "sort")+txt
        mC = result_dir+rev.replace("rev", "only5mC")+txt
        CHH = result_dir+rev.replace("rev", "CHH")+txt
        CG = result_dir+rev.replace("rev", "CG")+txt
        CHG = result_dir+rev.replace("rev", "CHG")+txt
        # extract forw, rev file, and generate corresponding file names


        os.system('cat {} {} > -q {}'.format(forw, rev, merge))
        os.system('sort {} -o {}'.format(merge, sort))
        os.system('awk {sum+=$6} END {print "Average for " FILENAME "=", sum/NR} {}'.format(sort))        #FIXME: Nc12genome hard coded. change to param?
        os.system('awk END {print NR} {}'.format(sort))
        os.system('awk $6>0 {} > {}'.format(sort, mC))
        os.system('awk {sum+=$6} END {print "Average reads for "FILENAME" = ", sum/NR}'.format(sort))
        os.system('grep CHH {} > {} '.format(sort,CHH))
        os.system('grep CG {} > {}'.format(sort, CG))
        os.system('grep CHG {} > {}'.format(sort, CHG))
        os.system('awk END {print NR } {}'.format(CHH))
        os.system('awk END {print NR } {}'.format(CG))
        os.system('awk END {print NR } {}'.format(CHG))



if __name__ == "__main__":
    '''
    Set default values for various parameters. Run from the command line.
    '''
    if len(sys.argv) < 1:
        print("""Usage:  {} <file_dir> <result_dir>""".format(sys.argv[0]))
        exit(1)
    parser = argparse.ArgumentParser(description="analysis for 5mC files")
    parser.add_argument("FILE_dir", type=str, help="directory folder contains source files")
    parser.add_argument("RESULT_dir", type=str, help="directory folder to store result files")
    args = parser.parse_args()
    file = args.FILE_dir
    result = args.RESULT_dir
    stepAnalyzing(file, result)