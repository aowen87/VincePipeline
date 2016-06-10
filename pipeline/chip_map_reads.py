'''
Created on June 7, 2016
​
@author: Pat Johnson
'''

import os
import sys
from sys import argv
from glob import glob

def map_reads(data_directory, genome, output_directory):
	"""
	Pipeline to map reads for IGV (from Chip-Seq)
	Arguments:
		data_directory: folder that contains reads
		genome:			either a fasta file or a folder containing a built genome
						If genome is a fasta file, then the genome is built
	"""
	
	#output directory folders
	os.mkdir(output_directory)
	os.mkdir(output_directory+"/samFiles")
	os.mkdir(output_directory+"/bam1")
	os.mkdir(output_directory+"/rdbam")
	os.mkdir(output_directory+"/results")
	
	#build genome if necessary from .fasta file
	if genome.endswith(".fasta"):
		os.mkdir(output_directory+"/GenomeFiles")
		output_genome = output_directory+"/GenomeFiles/" + genome[0:-6] + '_genome'
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
	 
		os.system("bowtie2 -p 12 -x {GENOME} -U {IN} -S {OUT}.sam".format(GENOME=output_genome, IN=files,
				OUT=output_directory+"/samFiles/"+file_name))
		
		os.system("samtools view -bS {IN}.sam > {OUT}.bam".format(IN=output_directory+"/samFiles/"+file_name,
				OUT=output_directory+"/bam1/"+file_name))
				
		os.system("samtools rmdup -s {IN}.bam {OUT}_rd.bam".format(IN=output_directory+"/bam1/"+file_name,
				OUT=output_directory+"/rdbam/"+file_name))
		
		os.system("samtools sort {IN}_rd.bam {OUT}_sort".format(IN=output_directory+"/rdbam/"+file_name,
				OUT=output_directory+"/results/"+file_name))
		
		os.system("samtools index {IN}_sort.bam".format(IN=output_directory+"/results/"+file_name))

			
if __name__ == "__main__":
	if len(argv) < 4:
		print("Usage:  {} data_directory genome output_directory".format(argv[0]))
		exit(1)
	data_directory = argv[1]
	genome = argv[2]
	output_directory = argv[3]
	map_reads(data_directory, genome, output_directory)
	
