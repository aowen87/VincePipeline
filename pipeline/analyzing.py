__author__ = 'Alister Maguire, xi'
__date__ = '04/24/2016'
__description__ = """The first in a sequence of functions designed
to pipeline Mike Roundtree's BS-seq protocol.
Generated statistics for 5mC level, CHH, CG, CHG files. """

import os
import sys
import argparse
import glob



def stepAnalyzing(fileDir, resultsDir, clean):
    """
    The step for analyzing the final BRAT ACGT count 5mC output files.
    args: fileDir (a directory containing 5mC forward and reverse files -> str)
          resultsDir (a target directory to move results into -> str)
          clean (clean up extraneous output -> boolean) 
    """

    if not os.path.isdir(resultsDir):
        os.system('mkdir {}'.format(resultsDir))
        
    avgPath = resultsDir + '/5mCAverages'
    if not os.path.isdir(avgPath):
        os.system('mkdir {}'.format(avgPath))
        
    wigPath = resultsDir + '/wigFiles'
    if not os.path.isdir(wigPath):
        os.system('mkdir {}'.format(wigPath))
        
    mergedPath = resultsDir + '/mergedFiles'
    if not os.path.isdir(mergedPath):
        os.system('mkdir {}'.format(mergedPath))

    mCfiles = [fileDir for fileDir in glob.glob('./{}/*.txt'.format(fileDir))]
    mCfiles.sort()
    fileLen = len(mCfiles)
    if fileLen%2!=0:
        fileLen-=1

    for i in range(0, fileLen, 2):
        forw    = mCfiles[i]
        rev     = mCfiles[i+1]
        fileID  = forw.split('_')[2] + '_' + forw.split('_')[3]
        avgFile = avgPath + '/' + fileID
        wigFile = wigPath + '/' + fileID + '.wig'
        os.system('touch {}'.format(avgFile))
        
        unProcMerge = rev.replace("rev", "unProcMerge").replace(fileDir, resultsDir)
        merged      = rev.replace("rev", "merged").replace(fileDir, resultsDir)
        sort        = rev.replace("rev", "sort").replace(fileDir, resultsDir)
        mC          = rev.replace("rev", "only5mC").replace(fileDir, resultsDir)
        CHH         = rev.replace("rev", "CHH").replace(fileDir, resultsDir)
        CG          = rev.replace("rev", "CG").replace(fileDir, resultsDir)
        CHG         = rev.replace("rev", "CHG").replace(fileDir, resultsDir)
         
        os.system('cat {} {} > {}'.format(forw, rev, unProcMerge))
        os.system("sed 's/:/\t/g' {} > {}".format(unProcMerge, merged))
        os.system('cp {} {}'.format(merged, mergedPath))
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
        os.system('rm {}/*.txt'.format(resultsDir))
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
    if len(sys.argv) < 3:  
        print("""Usage:  {} <fileDir> <resultsDir> <clean>""".format(sys.argv[0]))
        sys.exit(1)
    parser = argparse.ArgumentParser(description="analysis for 5mC files")
    parser.add_argument("fileDir", type=str, help="directory folder contains source files")
    parser.add_argument("resultsDir", type=str, help="directory folder to store resultsDir files")
    parser.add_argument('clean', type=bool, help="Would you like to remove all files output files not used further on?")
    args = parser.parse_args()
    fileDir = args.fileDir
    resultsDir = args.resultsDir
    clean = args.clean
    stepAnalyzing(fileDir, resultsDir, clean)
    
    