__author__ = 'Hiranmayi Duvvuri'
__date__ = '05/07/2016'
__description__ = """
Prepare BRAW-BW output files for analysis in methylation pipeline.
"""

import os, sys, glob, argparse

def convert_meth_file(input_dir, output_dir):
    """
    convert the BRAT-BW output file to match the Meth-Pipe format. next, convert to a .meth file.
    run HyperMR analysis producing a .bed file.
    requires methpipe to be loaded.
    args:
        input_dir: BRAT-BW output files (where : was replaced with a tab)
        output_dir: location to save .meth and .bed files
    """
    if not os.path.exists(output_dir):
        os.system()
        print(output_dir + ' created')

    tabbed_files = [x for x in glob.glob('{}/*_sorted.txt'.format(input_dir))]

    for i in tabbed_files:
        strain = i.split('/')[-1].split('_')[2]
        print('strain: ' + strain)
        meth_file = '{}/5mC_{}_methylpipe'.format(output_dir, strain)

        print('converting ' + i.split('/')[-1])

        os.system("cut -f1,2,4,5,6,7 {} > {}.txt".format(i, meth_file))
        os.system("awk '{{print $1,$2,$6,$3,$5,$4}}' {}.txt > {}_new.txt".format(meth_file, meth_file))
        os.system("rm {}.txt".format(meth_file))
        os.system("mv {}_new.txt {}.txt".format(meth_file, meth_file))
        os.system("sed -i 's/CHH/CG/g' {}.txt".format(meth_file))
        os.system("sed -i 's/CHG/CG/g' {}.txt".format(meth_file))
        os.system("LC_ALL=C sort -k 1,1 -k 3,3n -k 2,2n -k 6,6 -o {}_sorted.txt {}.txt".format(meth_file, meth_file))
        os.system("awk '{{$5 = 1-$5 ; print $0}}' {}_sorted.txt > {}_inverted.meth".format(meth_file, meth_file))
        print('finding hypo-methylated regions')
        os.system("hmr -o {}_inverted.hmr {}_inverted.meth".format(meth_file, meth_file))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Run methylation analysis pipeline on BRAT-BW files. Load methpipe before use.')
    parser.add_argument("meth_dir", 
                        type = str, 
                        help = "folder with BRAT-BW output files")
    parser.add_argument("meth_pipe_out", 
                        type = str, 
                        help = "output directory for .meth and .bed files")

    args = parser.parse_args()

    convert_meth_file(args.meth_dir, args.meth_pipe_out)