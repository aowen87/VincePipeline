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


def stepAnalyzing(file_dir, result_dir):
    """
    The step for analyzing the final BRAT ACGT count 5mC output files.
    """

    if os.path.isdir(result_dir):
        print("\n{} already exists...".format(result_dir))
        cont = input("\nUsing this directory may result in current files being replaced. Would you like to continue? (y/n) ")
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
        rev  = mCfiles[i+1]

        unProcMerge = rev.replace("rev", "unProcMerge").replace(file_dir, result_dir)
        merged      = rev.replace("rev", "merged").replace(file_dir, result_dir)
        sort        = rev.replace("rev", "sort").replace(file_dir, result_dir)
        mC          = rev.replace("rev", "only5mC").replace(file_dir, result_dir)
        CHH         = rev.replace("rev", "CHH").replace(file_dir, result_dir)
        CG          = rev.replace("rev", "CG").replace(file_dir, result_dir)
        CHG         = rev.replace("rev", "CHG").replace(file_dir, result_dir)
        # extract forw, rev file, and generate corresponding file names
         
        os.system('cat {} {} > {}'.format(forw, rev, unProcMerge))
        os.system("sed 's/:/\t/g' {} > {}".format(unProcMerge, merged))
        os.system('sort {} -o {}'.format(merged, sort))
        os.system("""awk '{sum+=$6} END {print "Average for " FILENAME "= ",sum/NR}' """ + sort)
        os.system("awk 'END {{print NR}}' {}".format(sort))
        os.system("awk '$6>0' {} > {}".format(sort, mC))
        os.system("""awk '{sum+=$6} END {print "Average for " FILENAME "= ",sum/NR}' """ + mC)
        os.system("""awk '{sum+=$5} END {print "Average reads for " FILENAME "= ",sum/NR}' """ + sort)
        
        os.system('grep CHH {} > {} '.format(sort,CHH))
        os.system('grep CG {} > {}'.format(sort, CG))
        os.system('grep CHG {} > {}'.format(sort, CHG))
        
        os.system("""awk '{sum+=$6} END {print "Average for " FILENAME "= ",sum/NR}' """ + CHH)
        os.system("""awk '{sum+=$6} END {print "Average for " FILENAME "= ",sum/NR}' """ + CG)
        os.system("""awk '{sum+=$6} END {print "Average for " FILENAME "= ",sum/NR}' """ + CHG)
        
        os.system("awk 'END {{print NR }}' {}".format(CHH))
        os.system("awk 'END {{print NR }}' {}".format(CG))
        os.system("awk 'END {{print NR }}' {}".format(CHG))
        

if __name__ == "__main__":
    '''
    Set default values for various parameters. Run from the command line.
    '''
    if len(sys.argv) < 2:  
        print("""Usage:  {} <file_dir> <result_dir>""".format(sys.argv[0]))
        exit(1)
    parser = argparse.ArgumentParser(description="analysis for 5mC files")
    parser.add_argument("FILE_dir", type=str, help="directory folder contains source files")
    parser.add_argument("RESULT_dir", type=str, help="directory folder to store result files")
    args = parser.parse_args()
    file = args.FILE_dir
    result = args.RESULT_dir
    stepAnalyzing(file, result)