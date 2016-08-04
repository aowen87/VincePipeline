----------------------------Methylation Pipeline------------------------------
Author:  Hiranmayi Duvvuri, Alister Maguire
contact: hiranmayid8@gmail.com, aom@uoregon.edu

    This pipeline contains the methylation pipeline from Mike Rountree's 
BS-seq protocol. This section prepares the files output from the BRAT-BW 
pipeline for use in the rest of the methylation pipeline. The pipeline is 
contained in the main GUI along with the BRAT-BW section of the pipeline.


Set-up: 
    In order to successfully run the meth-pipeline, 
a directory on ACISS must contain the BRAT-BW output
and the following files:
    
    sub-directories:
        <brat_bw_files>      This directory contains the output from
                             BRAT-BW pipeline with the merged .txt files. 
                             You can name this however you like; 
                             just be sure to remember the name of the
                             directory, for it will be required when 
                             running the pipeline from the GUI. 
       
        <meth_files>         This directory contains the output from the
                             meth_convert.py, or the .meth/.hmr files produced.
                             If running the methylome comparison or average 
                             methylation pipelines separately this will be the
                             input for both of those. If running the whole
                             meth-pipeline, then this is the output from
                             the first section.

    files:
        <meth_convert.py>    This is the source code for preparing
        				             the BRAT-BW output files for use in the 
                             meth-pipe. This file should only be altered 
                             by those who are familiar with python and 
                             modular programming. 

      <methylome_compare.py> This is the source code for comparing different
                             methylomes to a wild type/given sample.  
                             This file should only be altered by those 
                             who are familiar with python and modular 
                             programming. 
        
       <pbs files>           This file evokes one or all of the .py 
                             files given specific terminal arguments. 
       					             IMPORTANT: This file must be named
                             following the guidelines, and the following
                             contents placed in the header 
                             (note that <directory_path> should
                             be replaced with the path to the pipeline
                             directory):

                             #!/bin/bash 
                             #PBS -q generic
                             #PBS -m abe

                             module load python/3.4.4
                             module load methpipe

                             cd <directory_path>



                             For naming and filling in the rest of the file
                             contents, name each file exactly as listed for
                             the contents:


                             meth_pipe.pbs

                             python3 meth_convert.py ${input} ${output}
                             python3 methylome_comp.py ${input} ${output} ${wt_meth} ${wt_hmr}
                             python3 average_meth.py ${txt_directory} ${roi} ${linkage} ${window}


                             meth_convert.pbs

                             python3 meth_convert.py ${input} ${output} 



                             methy_compare.pbs

                             python3 methylome_comp.py ${input} ${output} ${wt_meth} ${wt_hmr}



                             ave_meth.pbs

                             python3 average_meth.py ${txt_directory} ${roi} ${linkage} ${window}



                             conv_comp.pbs

                             python3 meth_convert.py ${input} ${output}
                             python3 methylome_comp.py ${input} ${output} ${wt_meth} ${wt_hmr}



                             conv_avg.pbs

                             python3 meth_convert.py ${input} ${output}
                             python3 average_meth.py ${txt_directory} ${roi} ${linkage} ${window}



                             comp_avg.pbs

                             python3 methylome_comp.py ${input} ${output} ${wt_meth} ${wt_hmr}
                             python3 average_meth.py ${txt_directory} ${roi} ${linkage} ${window}

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

       .meth Conversion:       This tab contains the information for meth_convert.py

                    converted files directory         This directory contains the files from 
                                                      mergedFiles in the BRAT-BW pipeline.

                    results directory                 This directory will contain the results
                                                      from meth_convert.py in the form of the
                                                      .hmr and .meth files.
                                                      Files are output in the following format:
                                                      prefix_strand_suffix
                                                      These files will be used in the rest of the
                                                      methylation pipeline.

      methylome comparison:     This tab contains the information for methylome_comp.py

                      meth conversion directory       This directory contains the output from
                                                      meth_convert.py, or the .hmr and .meth files
                                                      for each sample.

                      results directory               This directory will contain the results from
                                                      methylome_comp.py outputting .methdiff files
                                                      as well as files containing the scores from
                                                      sample 1 and sample 2 with sample 1 being the
                                                      wild type or given sample and sample 2 being the
                                                      samples in the input directory.

                      .meth WT sample                 This is the .meth file of the sample all other
                                                      samples will be compared to.

                      .hmr WT sample                  This is the .hmr file of the sample all other
                                                      samples will be compared to.

    Notes:
        Every time a qsub job is run, there are 2 output files created as records
    from the job. Currently, these files are not removed with the 'remove extra output'
    option. These files contain records of the processes which can be looked over after
    the jobs have finished execution and are very helpful for determining problems that
    may have occurred. That being said, you'll probably want to remove them or they will 
    continue building up. 