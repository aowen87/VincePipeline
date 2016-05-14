__author__ = 'Hiranmayi Duvvuri'
__date__ = '05/10/2016'
__description__ = """
Compare methylomes and return the differential methylation scores between the two.
"""

import os, sys, glob, argparse

# compare mutants to a control/wildtype
def diff_comp(input_dir, output_dir, compare_all = True, wt = None, mut = None):
    """
    begin running Meth-Pipe on converted meth-pipe file. 
    and look at the differential methylation scores between two samples. 
    args:
        input_dir: files to compare control to
        output_dir: location to save comparisons
        compare_all: compare all .meth files if True
        wt: wildtype or control file
        mut: mutant file if only comparing one
    returns two files with differentially methylated regions identified.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mut_files = [x for x in glob.glob('{}/*.meth'.format(input_dir))]

    if compare_all and wt != None:
        for i in mut_files:
            s1 = wt.split('/')[-1].split('_')[1]
            s2 = i.split('/')[-1].split('_')[1]

            os.system("methdiff -o {}/{}vs{}.methdiff {} {}".format(output_dir, s1, s2, wt, j))
            os.system("dmr {}/{}vs{}.methdiff {}/{}_inverted.hmr {}/{}_inverted.hmr {}/DMR_{}vs{}_lt_{} {}/DMR_{}vs{}_lt_{}".format(output_dir, s1,
                s2, output_dir, s1, output_dir, s2, output_dir, s1, s2, s1, output_dir, s1, s2, s2))
    else:
        if wt and mut != None:
            s1 = wt.split('/')[-1].split('_')[1]
            s2 = mut.split('/')[-1].split('_')[1]

            os.system("methdiff -o {}/{}vs{}.methdiff {} {}".format(output_dir, s1, s2, wt, mut))
            os.system("dmr {}/{}vs{}.methdiff {}/{}_inverted.hmr {}/{}_inverted.hmr {}/DMR_{}vs{}_lt_{} {}/DMR_{}vs{}_lt_{}".format(output_dir, s1,
                s2, output_dir, s1, output_dir, s2, output_dir, s1, s2, s1, output_dir, s1, s2, s2))
        else:
            ValueError("please enter two files to compare")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Compare methylomes to a control/wild type sample')
    parser.add_argument("mut_input", 
                        nargs = '?',
                        type = str, 
                        help = "directory containing files to compare to control",
                        default = None)
    parser.add_argument("comp_dir", 
                        nargs = '?',
                        type = str, 
                        help = "output directory for differential methylation scores",
                        default = None)
    parser.add_argument("-c" "compare_all", 
                        nargs = '?',
                        help = "if True, compare all .meth files in directory. If False, only compare given files", 
                        default = True)
    parser.add_argument("wt",
                        help = "first of two .meth files to compare", 
                        default = None)
    parser.add_argument("mut", 
                        nargs = '?',
                        help = "Only required", 
                        default = None)

    args = parser.parse_args()

    diff_comp(args.meth_pipe_dir, args.comp_dir, args.compare_all, args.sample_1, args.sample_2)
