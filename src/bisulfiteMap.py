'''
Created on Apr 24, 2016

The first in a sequence of functions designed
to pipeline Mike Roundtree's BS-seq protocol.

This particular function runs BRAT-BW to map
bisulfite-seq reads.

@author: alister
'''
import os
import sys
import argparse
import glob
from collections import defaultdict


def bisulfiteMap(BRAT_genome_dir, fastq_dir, result_dir, build, non_BS_mismatches, quality_score):  
    '''
    Run BRAT-BW to map bisulfite-seq reads.
    args: BRAT_genome_dir (a reference BRAT_genome_dir -> str)
          fastq_dir (a directory path containing the fastq files to be mapped -> str)
          result_dir (a target directory for the end of the pipeline -> str)
          build (whether or not the reference BRAT_genome_dir needs to be built -> bool)
          non_BS_mismatches (the number of non-BS mismatches -> int)
          quality_score (the quality score -> int)
    '''
    
    if os.path.isdir(result_dir):
        print("\n{} already exists...".format(result_dir))
        cont = input("\nUsing this directory may result in current files being replaced. Would you like to continue? (y/n) ")
        if cont != 'y':
            sys.exit("\nEXITING\n")
    
    #FIXME:
    #check to see if file 'mappedDupl' exists. If not, create it and add 
    #the text 'BSmapped.txt'. 
    #Check to see if 'mappedNoDupl' exists. If not, create it and add 
    #the text 'BSmapped.txt.nodupl'.
    else:
        os.system('mkdir {}'.format(result_dir))
    
    fastqFiles = [file for file in glob.glob('./{}/*.fastq'.format(fastq_dir))]
    
    if build:
        os.system('build_bw -P {}'.format(BRAT_genome_dir))
        os.system('build_bw -P {} -G 2 -r {}'.format(BRAT_genome_dir, BRAT_genome_dir)) 
    
    strand_count = defaultdict(int)
    for f in fastqFiles:
        strand = f.split("_")[1].split("-")[0]
        strand_count[strand] += 1
        os.system('trim -s {} -P N{}_{} -q {} -m {}'.format(f, strand, strand_count[strand], quality_score, non_BS_mismatches))
        os.system('brat_bw -P {} -s N{}_{}_reads1.txt -o BSmapped.txt -W -C -m {}'.format(BRAT_genome_dir, strand, strand_count[strand], non_BS_mismatches)) 
        os.system('remove-dupl -r Nc12genome -s mappedDupl')  
        os.system('acgt-count -r Nc12genome -P 5mC_BSmapped_N{}_{} -s mappedNoDupl -B').format(strand, strand_count[strand])       
        os.system('mv 5mC_BSmapped_N{}_{}_forw.txt {}'.format(strand, strand_count[strand], result_dir))    
        os.system('mv 5mC_BSmapped_N{}_{}_rev.txt {}'.format(strand, strand_count[strand], result_dir)) 
        os.system('rm *.nodupl')
        #NOTE: may need to alter other file names if they are needed further down the pipeline.
        
if __name__ == "__main__":
    '''
    Set default values for various parameters. Run from the command line. 
    '''
    if len(sys.argv) < 3:
        print("""Usage:  {} <BRAT_genome_dir> <fasq_dir> <result_dir> <build=False> 
        <non_BS_mistmatches=2> <quality_score=20>""".format(sys.argv[0]))
        exit(1)
    parser = argparse.ArgumentParser(description="run BRAT-BW to map bisulfite-seq reads")
    parser.add_argument('BRAT_genome', type=str, help='a BRAT-BW genome directory')
    parser.add_argument('fastq_dir', type=str, help='a directory containing fastq files of bisulfite-seq reads')
    parser.add_argument('result_dir', type=str, help='the directory where the protocol results will be stored')
    parser.add_argument('build', action='store_false', help='Do you need to build a genome? default=False')
    parser.add_argument('non_BS_mismatches', type=int, nargs='?', default=2, help='specify the number of non-BS mismatches. default=2')
    parser.add_argument('quality_score', type=int, nargs='?', default=20, help='quality score. default=20')
    args = parser.parse_args()
    genome = args.BRAT_genome
    fastFile = args.fastq_dir
    result_dir = args.result_dir
    build = args.build
    m = args.non_BS_mismatches
    qs = args.quality_score
    bisulfiteMap(genome, fastFile, result_dir, build, m, qs)

