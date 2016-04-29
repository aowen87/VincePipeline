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


def bisulfiteMap(BRAT_genome_dir, fastq_dir, strand_name, result_dir, build, non_BS_mismatches, quality_score):  
    '''
    Run BRAT-BW to map bisulfite-seq reads.
    args: BRAT_genome_dir (a reference BRAT_genome_dir -> str)
          fastq_dir (a directory path containing the fastq files to be mapped -> str)
          strand_name (the name of the strand; will be appended to file names -> str)
          result_dir (a target directory for the end of the pipeline -> str)
          build (whether or not the reference BRAT_genome_dir needs to be built -> bool)
          non_BS_mismatches (the number of non-BS mismatches -> int)
          quality_score (the quality score -> int)
    '''
    
    if os.path.isdir(result_dir):
        print("\n{} already exists...".format(result_dir))
        cont = input("\nUsing this directory may result in current files being replaced. Would you like to continue? (y/n)")
        if cont != 'y':
            sys.exit("\nEXITING\n")
    else:
        os.system('mkdir {}'.format(result_dir))
    
    fastqFiles = [file for file in glob.glob('./{}/*.fastq'.format(fastq_dir))]
    
    #os.system('load brat/2.0.1')  FIXME: can't seem to effectively evoke from python. May need to evoke a bash
    #                                     script using 'source module load ...
    if build:
        os.system('build_bw -P {}'.format(BRAT_genome_dir))
        os.system('build_bw -P {} -G 2 -r {}'.format(BRAT_genome_dir, BRAT_genome_dir)) 
    count = len(fastqFiles)
    for i in range(count):
        os.system('trim -s {} -P {} -q {} -m {}'.format(fastqFiles[i], strand_name, quality_score, non_BS_mismatches))
        os.system('brat_bw -P {} -s {}_reads1.txt -o BSmapped.txt -W -C -m {}'.format(BRAT_genome_dir, strand_name, non_BS_mismatches)) 
        os.system('remove-dupl -r Nc12genome -s BSmapped.txt'.format(BRAT_genome_dir))                      #FIXME: BRAT_genome_dir file hard coded. change to param?
        os.system('acgt-count -r Nc12genome -P 5mC_BSmapped -s 5mC_BSmapped_forw.txt -B')                     # same as above ^
        os.system('acgt-count -r Nc12genome -P 5mC_BSmapped -s 5mC_BSmapped_rev.txt -B')                      # same as above ^
        os.system('mv 5mC_BSmapped_forw.txt 5mC_BSmapped_forw_{}.txt'.format(i))  
        os.system('mv 5mC_BSmapped_rev.txt 5mC_BSmapped_rev_{}.txt'.format(i))
        os.system('mv 5mC_BSmapped_forw_{}.txt {}'.format(i, result_dir))    
        os.system('mv 5mC_BSmapped_rev_{}.txt {}'.format(i, result_dir)) 
        #NOTE: may need to alter other file names if they are needed further down the pipeline.

if __name__ == "__main__":
    '''
    Set default values for various parameters. Run from the command line. 
    '''
    if len(sys.argv) < 4:
        print("""Usage:  {} <BRAT_genome_dir> <fasq_dir> <strand_name> <result_dir> <build=False> 
        <non_BS_mistmatches=2> <quality_score=20>""".format(sys.argv[0]))
        exit(1)
    parser = argparse.ArgumentParser(description="run BRAT-BW to map bisulfite-seq reads")
    parser.add_argument('BRAT_genome', type=str, help='a BRAT-BW genome directory')
    parser.add_argument('fastq_dir', type=str, help='a directory containing fastq files of bisulfite-seq reads')
    parser.add_argument('strand_name', type=str, help='the name of the strand')
    parser.add_argument('result_dir', type=str, help='the directory where the (entire) pipeline results will be stored')
    parser.add_argument('build', action='store_false', help='Do you need to build a genome? default=False')
    parser.add_argument('non_BS_mismatches', type=int, nargs='?', default=2, help='specify the number of non-BS mismatches. default=2')
    parser.add_argument('quality_score', type=int, nargs='?', default=20, help='quality score. default=20')
    args = parser.parse_args()
    genome = args.BRAT_genome
    strand = args.strand_name
    fastFile = args.fastq_dir
    result_dir = args.result_dir
    build = args.build
    m = args.non_BS_mismatches
    qs = args.quality_score
    bisulfiteMap(genome, fastFile, strand, result_dir, build, m, qs)

