__author__ = 'Hiranmayi Duvvuri'
__date__ = '05/10/2016'
__description__ = """
Compare methylomes and return the differential methylation scores between the two.
"""

import os, sys, glob, argparse

# compare mutants to a control/wildtype
def diff_comp(input_dir, output_dir, wt_meth = None, wt_hmr = None):
    """
    begin running Meth-Pipe on converted meth-pipe file. 
    and look at the differential methylation scores between two samples. 
    args:
        input_dir: .hmr and .meth files to compare control to
        output_dir: location to save comparisons
        compare_all: compare all .meth files if True
        wt: wildtype or control file
        mut: mutant file if only comparing one
    returns two files with differentially methylated regions identified.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(output_dir + ' created')

    mut_meth = [x for x in glob.glob('{}/*.meth'.format(input_dir))]
    mut_hmr = [x for x in glob.glob('{}/*.hmr'.format(input_dir))]

    if wt_meth != None and wt_hmr != None:
        for i, j in zip(mut_meth, mut_hmr):
            s1 = wt_meth.split('/')[-1].split('_')[1]
            s2 = i.split('/')[-1].split('_')[1]

            print('finding differential methylation scores between {} and {}...'.format(s1, s2))

            os.system("methdiff -o {}/{}vs{}.methdiff {} {}".format(output_dir, s1, s2, wt_meth, i))

            print('finding DMRs between {} and {}...'.format(s1, s2))

            os.system("dmr {}/{}vs{}.methdiff {} {} {}/DMR_{}vs{}_lt_{} {}/DMR_{}vs{}_lt_{}".format(output_dir, s1,
                        s2, wt_hmr, j, output_dir, s1, s2, s1, output_dir, s1, s2, s2))
    else:
        raise ValueError("please enter a")

def main():

    if len(sys.argv) > 4:
        print("usage: {} <input_dir> <output_dir> <wt_meth> <wt_hmr>".format(sys.argv[0]))
        sys.exit(1)

    parser = argparse.ArgumentParser(description = 'Compare methylomes to a control/wild type sample')
    parser.add_argument("mut_input", 
                        type = str, 
                        help = "directory containing files to compare to control")
    parser.add_argument("comp_dir", 
                        type = str, 
                        help = "output directory for differential methylation scores")
    parser.add_argument("wt_meth",
                        help = "control .meth file", 
                        default = None)
    parser.add_argument("wt_hmr", 
                        help = "control .hmr file", 
                        default = None)

    args = parser.parse_args()

    diff_comp(args.mut_input, args.comp_dir, args.wt_meth, args.wt_hmr)

if __name__ == '__main__':
    main()
