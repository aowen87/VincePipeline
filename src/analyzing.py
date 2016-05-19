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


def stepAnalyzing(file_dir, result_dir, clean):
    """
    The step for analyzing the final BRAT ACGT count 5mC output files.
    args: file_dir (a directory containing 5mC forward and reverse files -> str)
          result_dir (a target directory to move results into -> str)
          clean (clean up extraneous output -> boolean) 
    """

    if not os.path.isdir(result_dir):
        os.system('mkdir {}'.format(result_dir))
        
    avgPath = result_dir + '/5mCAverages'
    if not os.path.isdir(avgPath):
        os.system('mkdir {}'.format(avgPath))
        
    wigPath = result_dir + '/wigFiles'
    if not os.path.isdir(wigPath):
        os.system('mkdir {}'.format(wigPath))

    mCfiles  = [file for file in glob.glob('./{}/*.txt'.format(file_dir))]
    mCfiles.sort()
    file_len = len(mCfiles)
    if file_len%2!=0:
        file_len-=1

    for i in range(0, file_len, 2):
        forw = mCfiles[i]
        rev  = mCfiles[i+1]
        fileID = forw.split('_')[2] + '_' + forw.split('_')[3]
        avgFile = avgPath + '/' + fileID
        wigFile = wigPath + '/' + fileID + '.wig'
        os.system('touch {}'.format(avgFile))
        
        unProcMerge = rev.replace("rev", "unProcMerge").replace(file_dir, result_dir)
        merged      = rev.replace("rev", "merged").replace(file_dir, result_dir)
        sort        = rev.replace("rev", "sort").replace(file_dir, result_dir)
        mC          = rev.replace("rev", "only5mC").replace(file_dir, result_dir)
        CHH         = rev.replace("rev", "CHH").replace(file_dir, result_dir)
        CG          = rev.replace("rev", "CG").replace(file_dir, result_dir)
        CHG         = rev.replace("rev", "CHG").replace(file_dir, result_dir)
         
        os.system('cat {} {} > {}'.format(forw, rev, unProcMerge))
        os.system("sed 's/:/\t/g' {} > {}".format(unProcMerge, merged))
        os.system('sort {} -o {}'.format(merged, sort))
        os.system("""awk '{{sum+=$6}} END {{print "Average level of 5mC for {} = ",sum/NR}}' {} > {}""".format(fileID, sort,  avgFile))
        os.system("""awk 'END {{print "total cytosines: ", NR}}' {} >> {}""".format(sort, avgFile))
        os.system("awk '$6>0' {} > {}".format(sort, mC))
        os.system("""awk '{{sum+=$6}} END {{print "Average for {} with methyl level > 0 = ",sum/NR}}' {}  >> {}""".format(fileID, mC, avgFile))
        os.system("""awk '{{sum+=$5}} END {{print "Average reads for {} = ",sum/NR}}' {} >> {} """.format(fileID, sort, avgFile))
        
        os.system('grep CHH {} > {} '.format(sort,CHH))
        os.system('grep CG {} > {}'.format(sort, CG))
        os.system('grep CHG {} > {}'.format(sort, CHG))
        
        os.system("""awk '{{sum+=$6}} END {{print "Average 5mC for {} = ",sum/NR}}' {} >> {}""".format(fileID, CHH, avgFile))
        os.system("""awk '{{sum+=$6}} END {{print "Average 5mC for {} = ",sum/NR}}' {} >> {} """.format(fileID, CG, avgFile))
        os.system("""awk '{{sum+=$6}} END {{print "Average 5mC for {} = ",sum/NR}}' {} >> {} """.format(fileID, CHG, avgFile))
       

        os.system("""awk 'END {{print "total CHH: ", NR }}' {} >> {}""".format(CHH, avgFile))
        os.system("""awk 'END {{print "total CG: ", NR }}' {} >> {}""".format(CG, avgFile))
        os.system("""awk 'END {{print "total CHG: ", NR }}' {} >> {}""".format(CHG, avgFile))
    
        os.system('cut -f 1,2,3,6 {} > {}'.format(mC, wigFile))
        
    if clean:
        os.system('rm {}/*.txt'.format(result_dir))
        os.system('rm *.txt')
        os.system('rm *.fastq')
    else:
        if not os.path.isdir('otherOutput'):
            os.system('mkdir otherOutput')
        os.system('mv *.txt otherOutput')
        os.system('mv *.fastq otherOutput')
        

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
    parser.add_argument('clean', action='store_true', help="""Would you like to remove all files ouput files not used further on?""")
    args = parser.parse_args()
    file = args.FILE_dir
    result = args.RESULT_dir
    clean = args.clean
    stepAnalyzing(file, result, clean)
    
    