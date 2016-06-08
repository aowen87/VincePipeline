'''
Created on June 7, 2016
​
@author: Pat Johnson
'''

import os
import sys
from sys import argv
from glob import glob

def map_reads(data_directory, genome):
	"""
	Pipeline to map reads for IGV (from Chip-Seq)
	Arguments:
		data_directory: folder that contains reads
		genome:			either a fasta file or a folder containing a built genome
						If genome is a fasta file, then the genome is built
	"""
	
	#output directory folders
	os.mkdir("samFiles")
	os.mkdir("bam1")
	os.mkdir("rdbam")
	os.mkdir("RESULTS")
	
	#build genome if necessary from .fasta file
	if genome.endswith(".fasta"):
		os.mkdir("GenomeFiles")
		output_genome = "GenomeFiles/" + genome[0:-6] + '_genome'
		os.system("bowtie2-build {IN} {OUT}".format(IN=genome, OUT=output_genome))
	else:
		os.walk(genome)
		genome_files = glob(os.path.join(genome,'*.bt2'))
		output_genome = genome_files[0].split(".")[0]

	
	os.walk(data_directory)
	
	file_list = glob(os.path.join(data_directory,'*.fastq'))
	
	#command calls
	
	for files in file_list:
	
		file_name = os.path.basename(files)[0:-6]
	 
		os.system("bowtie2 -p 12 -x {GENOME} -U {IN} -S {OUT}.sam".format(GENOME=output_genome, IN=files, OUT="samFiles/"+file_name))
		
		os.system("samtools view -bS {IN}.sam > {OUT}.bam".format(IN="samFiles/"+file_name, OUT="bam1/"+file_name))
				
		os.system("samtools rmdup -s {IN}.bam {OUT}_rd.bam".format(IN="bam1/"+file_name, OUT="rdbam/"+file_name))
		
		os.system("samtools sort {IN}_rd.bam {OUT}_sort".format(IN="rdbam/"+file_name, OUT="RESULTS/"+file_name))
		
		os.system("samtools index {IN}_sort.bam".format(IN="RESULTS/"+file_name))

			
if __name__ == "__main__":
	if len(argv) < 3:
		print("Usage:  {} data_directory output_directory genome.fasta".format(argv[0]))
		exit(1)
	data_directory = argv[1]
	genome = argv[2]
	map_reads(data_directory, genome)
	
