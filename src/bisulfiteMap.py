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

#FIXME: pass result_directory here or handle elsewhere??
def bisulfiteMap(genome, build, fastFile, result_directory, m):  
    '''
    Run BRAT-BW to map bisulfite-seq reads.
    args: genome (a reference genome)
          build (whether or not the reference genome needs to be built)
          fastFile (a fastq file containing bisulfite-seq reads)
          result_directory (a target directory for the end of the pipeline)
          m (the number of non-BS mistmatches)
    returns: result_directory (TENTATIVE)
    '''
    try:
        os.system('load brat/2.0.1')
    except:
        sys.exit('problem loading brat') 
    if build:
        os.system('build_bw -P {}'.format(genome))
        os.system('build_bw -P {} -G 2 -r {}'.format(genome, genome)) 
    try:
        os.system('trim -s {} -P N5417 -q 20 -m {}'.format(fastFile, m))
        os.system('brat_bw -P Nc12_genome -s BStrim.txt -o BSmapped.txt -W -C -m {}'.format(m))
        os.system('remove-dupl -r {}.txt -s BSmapped.txt'.format(genome)) #genome.txt?????
        os.system('argt-count -r {} -P 5mC_BSmapped -s BSmapped_rd.txt -B'.format(genome))
    except:
        sys.exit("problem encountered while mapping")
    return result_directory


if __name__ == "__main__":
    '''
    Set default values for build and m arguments. Run from the command line. 
    '''
    parser = argparse.ArgumentParser(description="run BRAT-BW to map bisulfite-seq reads")
    parser.add_argument('genome', type=str, help='a complete genome to map reads to')
    parser.add_argument('build', type=bool, action='store_false', help='Do you need to build a genome? default=False')
    parser.add_argument('fastFile', type=str, help='a fastq file containing bisulfite-seq reads')
    parser.add_argument('result_directory', type=str, help='the directory where the (entire) pipeline results will be stored')
    parser.add_argument('m', type=int, nargs='?', default=2, help='specify the number of non-BS mismatches. default=2')
    args = parser.parse_args()
    genome = args.genome
    build = args.build
    fastFile = args.fastFile
    result_directory = args.result_directory
    m = args.m
    bisulfiteMap(genome, build, fastFile, result_directory, m)

