----------------------------BRAT-BW pipe------------------------------
Author:  Alister Maguire
contact: aom@uoregon.edu

    This pipeline contains the first two sections from Mike Rountree's
BS-seq protocol. The first section, titled "Commands to run BRAT-BW to 
map bisulfite-seq reads," is contained within the python script
bisulfiteMap.py. The second section, titled "Steps for analyzing final
BRAT: ACGTcount 5mC output file," is contained with the python script
analyzing.py. Both sections are contained within a main GUI, which also 
contains other sections from the protocol that may be run separately.  


Set-up: 

    Python:
        
        Python 3.x must be installed for running this program. We suggest
    installing version 3.5 or later. Also, the package 'paramiko' must
    be installed. To see if paramiko is installed, open a terminal
    (powershell if on Windows), and type 'pip show paramiko'. If it's 
    installed, you should see the package details. Otherwise, you can 
    install paramiko with the following command 'pip install paramiko'. 

    
    ACISS:

        In order to successfully run the BRAT pipeline, 
    a directory must be created on ACISS that contains the 
    following sub-directories and files:
    
    sub-directories:
        <fastq_files>     This directory contains the fastq files
                          that you wish to perform the computations
                          on. You can name this however you like; 
                          just be sure to remember the name of the
                          directory, for it will be required when 
                          running the pipeline from the GUI. 
        
        <BS_genome_fasta> This is a directory containing supercontig
                          files. IMPORTANT: The name of this directory
                          must be exactly as depcited, or the pipeline
                          will not correctly run without altering 
                          the source code. 
                          
        <genome>     	  This is the genome that you wish to use
                          for the bisulfite mapping. There is an 
                          option for building the genome from scratch, 
                          but this should be tested before use to 
                          ensure that the genome is built as expected.
                          This directory can be named however you wish.

    files:
        <bisulfiteMap.py> This is the source code for running the 
                          first step of the bisulfite mapping.  
                          This file should only be altered by those 
                          who are familiar with python and modular 
                          programming. 

        <analyzing.py>    This is the source cod for the second step
                          in the bisulfite mapping. Again, this file 
                          should only be altered by those familiar with
                          python and modularity. 

        <mappedDupl>      IMPORTANT: This file must be named exactly 
                          as shown, and its contents must be as follows:
                          
                          ./BSmapped.txt
 
                          If this file is missing, the program will crash.
                          If the contents of this file are not exactly
                          as specified, the program will produce erroneous
                          results. 
                             
        <mappedNoDupl>    IMPORTANT: This file must be named exactly 
                          as shown, and its contents must be as follows:
                          
                          ./BSmapped.txt.nodupl
 
                          If this file is missing, the program will crash.
                          If the contents of this file are not exactly
                          as specified, the program will produce erroneous
                          results. 
        
        <Nc12genome>      This file contains the path to all of the
                          supercontig files. IMPORTANT: This file must
                          be named excactly as shown, or the program will
                          not run correctly without altering the source 
                          code. 
        
        <bratPipe.pbs>    This file evokes the bisulfiteMap.py and 
                          analyzing.py programs given specific terminal
                          arguments. IMPORTANT: This file must be named
                          exactly as shown, and the contents must be 
                          as follows (note that <directory_path> should
                          be replaced with the path to the pipeline
                          directory):

                          #!/bin/bash 
                          #PBS -q generic
                          #PBS -m abe
                          module load python/3.4.4
                          module load brat/2.0.1
                          cd <directory_path>
                          python3 bisulfiteMap.py ${brat} ${fastq} ${build} ${mismatch} ${score}  
                          python3 analyzing.py ${map} ${res} ${clean} 

    GUI Usage:
             The pipline is currently set-up to run through the given GUI, so this is 
        what will be explained regarding usage. 

        Email:                 If you'd like to recieve email notifications regarding 
                               when your job has begun and finished, you can fill in 
                               this window (not required). 

        ACISS user name:       This is the 'usrname' in usrname@aciss.uoregon.edu

        ACISS password:        If your ACISS account is set up for login without password 
                               verification, this window can be left empty. Otherwise, 
                               you must enter you password. 

        BRAT genome directory: This is the name of the genome directory title <genome> above. 
             
        fastq directory:       This is the directory containing the fastq files that you 
                               wish to send through the bisulfite mapping, titled
                               <fastq_files> above. 

        results directory:     This is the directory that will contain the final results of
                               the two protocols contained in analyzing.py and bisulfiteMap.py. 
                               You may name this directory whatever you wish upon execution. 
                               When the execution has completed, this results directory will
                               contain the following three subdirectories:
                               5mCAverages, mergedFiles, and wigFiles.
                               The files within mergedFiles are primarily for use further down
                               the pipeline. 5mCAverages contains output from analying.py, and
                               wigFiles contains the final wig files. All output files are of
                               the following format:
                               prefix_strand_occurrence_suffix.
                               prefix and suffix are both optional and only occur with some 
                               of the output files. occurrence denotes the number of times 
                               this particular strand was analyzed. 

        non-BS mismatches:     This is an integer as specified in Mike Rountree's protocol. 
                               The suggested input is 2, which has been made the default value. 
                               
        quality score:         This is also an integer as specified in Mike Rountree's protocol. 
                               The default input is 20. 

        build genome:          Check this box if you'd like to build your genome. IMPORTANT: this
                               should be tested before use. We have been using the genome given
                               to us for testing. If you have a genome already built and in the
                               pipeline directory, you can leave this box unchecked. 

        remove extra output:   Check this box if you'd like to remove extraneous output produced
                               throughout the protocol. Wig files, merged files, 5mC averages, 
                               and results from the bisulfite map are all saved regardless of 
                               whether or not this box is checked. The only files that are removed
                               are those which appeared to be of temporary use within the protocol. 
                               Therefore, this box is checked by default.


    Miscellaneous::

        Every time the a qsub job is run, there are 2 output files created as records
    from the job. Currently, these files are not removed with the 'remove extra output'
    option. These files contain records of the processes which can be looked over after
    the jobs have finished execution and are very helpful for determining problems that
    may have occurred. That being said, you'll probably want to remove them or they will 
    continue building up. 
