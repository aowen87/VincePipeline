import os
import sys
from sys import argv
from glob import glob

def methpipe(data_directory, roi_bed, linkage_groups, windowSize, output_directory):
	"""
	data_directory: name of a folder that contains sorted text files from Meth-pipe analysis
	roi_bed: name of bed file containing regions of interest
	LinkageGroup: Linkage group being looked at
	windowSize: desired window size for output window size
	
	"""
	os.mkdir(output_directory)
	os.mkdir(output_directory+"/tempFiles")
	os.mkdir(output_directory+"/results")
	os.mkdir(output_directory+"/tempFiles/stepwise")
	
	linkages = linkage_groups.split(",")
	
	linkage_sizes = {1:9798893, 2:4478683, 3:5274802, 4:6000761, 5:6436246, 6:4218384, 7:4255303}

	os.walk(data_directory)
	
	file_list = glob(os.path.join(data_directory,'*.txt'))
	
	for files in file_list:
	
		file_name = os.path.basename(files)[0:-4]		
		
		os.system("awk '{{print $0}}' {IN}.txt > {OUT}.meth".format(IN=data_directory + '/' + file_name, OUT=output_directory+"/tempFiles/"+file_name))
		
		os.system("LC_ALL=C sort -k 1,1 -k 3,3n -k 2,2n -k 6,6 -o {OUT}.sorted.bed {IN}".format(OUT=output_directory+"/tempFiles/"+roi_bed[0:-4], IN=roi_bed))
				
		os.system("roimethstat -o {OUT}_roi.bed {BED}.sorted.bed {METH}.meth".format(OUT=output_directory+"/results/"+file_name, BED=output_directory+"/tempFiles/"+roi_bed[0:-4],
																					METH=output_directory+"/tempFiles/"+file_name))
		
		for linkage in linkages:
			
			os.system("seq -f""%.0f"" 1 {WS} {SIZE} > {OUT}/Nc_LG{LG}_{WS}bp.txt".format(OUT=output_directory+"/tempFiles", WS=windowSize, SIZE=linkage_sizes[int(linkage)], LG=linkage))
		
			os.system("seq -f""%.0f"" {WS} {WS} {SIZE} > {OUT}/Nc_LG{LG}_{WS}bp2.txt".format(OUT=output_directory+"/tempFiles", WS=windowSize, SIZE=linkage_sizes[int(linkage)], LG=linkage))
		
			with open("{IN}/Nc_LG{LG}_{WS}bp.txt".format(IN=output_directory+"/tempFiles", WS=windowSize, LG=linkage)) as f:
				for file_lines, l in enumerate(f):
					pass
			
			file_lines += 1
		
			os.system("printf 'Supercontig_12.{LG}\n%.0s' {{1..{LINES}}} > {OUT}/Supercontig_12.{LG}_{WINDOW}bp.txt".format(OUT=output_directory+"/tempFiles", LG=linkage, WINDOW=windowSize, LINES=file_lines))
				
			os.system("printf '12.{LG}_\n%.0s' {{1..{LINES}}} > {OUT}/12.{LG}_{WINDOW}bp.txt".format(OUT=output_directory+"/tempFiles", LG=linkage, WINDOW=windowSize, LINES=file_lines))
		
			os.system("printf '+\n%.0s' {{1..{LINES}}} > {OUT}/12.{LG}+_{WINDOW}bp.txt".format(OUT=output_directory+"/tempFiles", LG=linkage, WINDOW=windowSize, LINES=file_lines))
		
			os.system("seq 1 {LINES} > {OUT}/12.{LG}#_{WINDOW}bp.txt".format(OUT=output_directory+"/tempFiles", LG=linkage, WINDOW=windowSize, LINES=file_lines))
		
			os.system("paste {OUT}/Supercontig_12.{LG}_{WINDOW}bp.txt {OUT}/Nc_LG{LG}_{WINDOW}bp.txt {OUT}/Nc_LG{LG}_{WINDOW}bp2.txt {OUT}/12.{LG}_{WINDOW}bp.txt {OUT}/12.{LG}#_{WINDOW}bp.txt {OUT}/12.{LG}+_{WINDOW}bp.txt > {OUT}/Nc12.{LG}_{WINDOW}bp.txt".format(OUT=output_directory+"/tempFiles", LG=linkage, WINDOW=windowSize))
		
		
			with open("{OUT}/Nc12.{LG}_{WINDOW}bp.txt".format(OUT=output_directory+"/tempFiles/stepwise", FILE_NAME=file_name, LG=linkage, WINDOW=windowSize), "w") as outfile:
				with open("{OUT}/tempFiles/Nc12.{LG}_{WINDOW}bp.txt".format(OUT=output_directory, LG=linkage, WINDOW=windowSize), "r") as infile:
					for line in infile:
						outfile.write(line.replace("_	", "_"))
					outfile.write("\n")
					
		
	step_wise = glob(os.path.join(output_directory+"/tempFiles/stepwise",'*.txt'))
	
	with open(output_directory+"/results/stepwise_Genome.txt", "w") as outfile:
		for f in step_wise:
			with open(f, "r") as infile:
				outfile.write(infile.read())
				
	os.system("awk '{{print $0}}' {IN}.txt > {OUT}.bed".format(IN=output_directory + '/results/stepwise_Genome', OUT=output_directory + '/results/stepwise_Genome'))
		

			
if __name__ == "__main__":
	if len(argv) < 6:
		print("Usage: {} data_directory roi_bed LinkageGroup windowSize output_directory".format(argv[0]))
		exit(1)
	data_directory = argv[1]
	roi = argv[2]
	lgs = argv[3]
	ws = argv[4]
	out = argv[5]
	methpipe(data_directory, roi, lgs, ws, out)
	
