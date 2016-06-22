----------------------------Chip-Seq pipe------------------------------
Author:	 Pat Johnson, Alister Maguire
contact: pwj@uoregon.edu (pj3394b@gmail.com), aom@uoregon.edu

	This pipeline map reads to a genome for dispay on IGV and
	is contained in the main GUI.


Set-up: 
	To run this pipeline, ensure that ACISS contains the 
	following folders and/or files:
	
	User input files/subdirectories:
		<data_directory>	 This directory contains all .fastq files you wish to
			                 to map to a single genome. Note that if you have .fastq
				         files you wish to map different genomes, you will have
				         run the pipeline multiple times, once for each genome.
	   
		<genome>		 This input can be either the directory of a built genome or 
					 or a .fasta file that you wish to build a genome from.	This
				         is the genome your .fastq files will be mapped to.

	files for running the program:
		<chip_map_reads.py>      This is the source code for mapping the
					 reads. This file should only be altered 
					 by those who are familiar with python and 
					 modular programming. 
		
	        <pbs files>		 This file evokes the .py file given specific 
					 terminal arguments. IMPORTANT: This file must be named
					 following the guidelines, and the following
					 contents placed in the header 
					 (note that <directory_path> should
					 be replaced with the path to the pipeline
					 directory):

					 #!/bin/bash 
					 #PBS -q generic
					 #PBS -m abe

					 module load python/3.4.4
					 module load bowties
					 module load samtools 

				         cd <directory_path>



				         For naming and filling in the rest of the file
				         contents, name each file exactly as listed for
				         the contents:


				         chip_pipe.pbs

				         python3 chip_map_reads.py ${chip_directory} ${genome}

	GUI Usage:
			 The pipline is currently set-up to run through the given GUI, so this is 
		what will be explained regarding usage. 

		Email:		           If you'd like to recieve email notifications regarding 
					   when your job has begun and finished, you can fill in 
				           this window (not required). 

		ACISS user name:	   This is the 'usrname' in usrname@aciss.uoregon.edu

		ACISS password:		   If your ACISS account is set up for login without password 
				           verification, this window can be left empty. Otherwise, 
					   you must enter you password. 

	        ChiP Reads:	           This tab contains the information for chip_map_reads.py

		Data Directory		   This directory contains the .fastq files.

		Output directory	   This directory will contain the resulting files. 


	Notes:
		Every time a qsub job is run, there are 2 output files created as records
	from the job. Currently, these files are not removed with the 'remove extra output'
	option. These files contain records of the processes which can be looked over after
	the jobs have finished execution and are very helpful for determining problems that
	may have occurred. That being said, you'll probably want to remove them or they will 
	continue building up.
