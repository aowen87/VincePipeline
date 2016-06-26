import sys
from unixInstall import *
from windowsInstall import *
from linuxInstall import *

def install(usrname, pswd, ACISS_path, shortcut_dest, genome_path):
    cur_os = str(sys.platform).lower()
    print(cur_os)#FIXME: remove after testing
    if cur_os[:6] == 'darwin':
        unixInstall(usrname, pswd, ACISS_path, shortcut_dest, genome_path)    
    elif cur_os[5] == 'linux':
        linuxInstall(usrname, pswd, ACISS_path, shortcut_dest, genome_path)    
    elif cur_os[:5] == 'win32' or cur_ow[:6] == 'cygwin':
        windowsInstall(usrname, pswd, ACISS_path, shortcut_dest, genome_path)
    else:
        print("ERROR: unsuported operating system")
        print("Check documentation for manual installation")
        sys.exit()


    
if __name__ == "__main__":
    '''
    '''
    parser = argparse.ArgumentParser("Setup for Vince's pipeline")
    parser.add_argument('usrname', type=str)
    parser.add_argument('pswd', type=str, default='')
    parser.add_argument('ACISS_path', type=str)
    parser.add_argument('shortcut_path', type=str)
    parser.add_argument('genome_path', type=str)
    args = parser.parse_args()
    usrname = args.usrname
    pswd = args.pswd 
    ACISS_path = args.ACISS_path
    shortcut_path = args.shortcut_path
    genome_path = args.genome_path
    install(usrname, pswd, ACISS_path, shortcut_path, genome_path)


