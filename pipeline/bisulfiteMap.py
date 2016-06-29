__author__ = 'Alister Maguire'
__date__ = '04/24/2016'
__description__ = """The first in a sequence of functions designed
to pipeline Mike Roundtree's BS-seq protocol.

This particular function runs BRAT-BW to map
bisulfite-seq reads. """


import os
import sys
import argparse
import glob
from collections import defaultdict


def bisulfiteMap(BRAT_genome_dir, fastq_dir, build, non_BS_mismatches, quality_score):  
    '''
    Run BRAT-BW to map bisulfite-seq reads.
    args: BRAT_genome_dir (a reference BRAT_genome_dir -> str)
          fastq_dir (a directory path containing the fastq files to be mapped -> str)
          build (whether or not the reference BRAT_genome_dir needs to be built -> bool)
          non_BS_mismatches (the number of non-BS mismatches -> int)
          quality_score (the quality score -> int)
    '''
    resultsDir = "mapResults" 
    if not os.path.isdir(resultsDir):
        os.system('mkdir {}'.format(resultsDir))
            
    if not os.path.isfile("mappedDupl"):
        print("ERROR: missing fileDir -> mappedDupl")
        sys.exit()
          
    if not os.path.isfile("mappedNoDupl"):
        print("ERROR: missing fileDir -> mappedNoDupl")
        sys.exit()
      
    fastqFiles = [fileDir for fileDir in glob.glob('./{}/*.fastq'.format(fastq_dir))]
    
    if build:
        os.system('build_bw -P {}'.format(BRAT_genome_dir))
        os.system('build_bw -P {} -G 2 -r {}'.format(BRAT_genome_dir, BRAT_genome_dir)) 
    
    strand_count = defaultdict(int)
    for f in fastqFiles:
        strand = f.split("_")[1].split("-")[0]
        strand_count[strand] += 1
        os.system('trim -s {} -P N{}_{} -q {} -m {}'.format(f, strand, strand_count[strand], quality_score, non_BS_mismatches))
        os.system('brat_bw -P {} -s N{}_{}_reads1.txt -o BSmapped.txt -W -C -m {}'.format(BRAT_genome_dir, strand, strand_count[strand], non_BS_mismatches)) 
        os.system('remove-dupl -r Nc12genome -s ./mappedDupl')  
        os.system('acgt-count -r Nc12genome -P 5mC_BSmapped_N{}_{} -s ./mappedNoDupl -B'.format(strand, strand_count[strand]))       
        os.system('mv 5mC_BSmapped_N{}_{}_forw.txt {}'.format(strand, strand_count[strand], resultsDir))    
        os.system('mv 5mC_BSmapped_N{}_{}_rev.txt {}'.format(strand, strand_count[strand], resultsDir)) 
        os.system('rm *.nodupl')
        
        
        
if __name__ == "__main__":
    '''
    Set default values for various parameters. Run from the command line. 
    '''
    if len(sys.argv) < 3:
        print("""Usage:  {} <BRAT_genome_dir> <fasq_dir> <build> 
        <non_BS_mistmatches=2> <quality_score=20>""".format(sys.argv[0]))
        sys.exit()
    parser = argparse.ArgumentParser(description="run BRAT-BW to map bisulfite-seq reads")
    parser.add_argument('BRAT_genome', type=str, help='a BRAT-BW genome directory')
    parser.add_argument('fastq_dir', type=str, help='a directory containing fastq files of bisulfite-seq reads')
    parser.add_argument('build', type=str, help='Do you need to build a genome? True/False')
    parser.add_argument('non_BS_mismatches', type=int, nargs='?', default=2, help="""specify the number of non-BS mismatches. default=2""")
    parser.add_argument('quality_score', type=int, nargs='?', default=20, help='quality score. default=20')
    args = parser.parse_args()
    genome = args.BRAT_genome
    fastFiles = args.fastq_dir
    build = args.build
    if build == 'False':
        build = False
    elif build == 'True':
        build = True
    else:
        print("ERROR: Invalid build value")
        sys.exit() 
    m = args.non_BS_mismatches
    qs = args.quality_score
    bisulfiteMap(genome, fastFiles, build, m, qs)

