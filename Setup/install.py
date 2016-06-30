import sys
import installer

def install(usrname, pswd, ACISS_path, shortcut_dest, genome_path):
    cur_os = str(sys.platform).lower()
    print(cur_os)#FIXME: remove after testing
    if cur_os == 'darwin':
        ins = installer.Installer('darwin')
    elif cur_os == 'linux':
        ins = installer.Installer('linux')
    elif cur_os == 'win32' or cur_os == 'cygwin':
        ins = installer.Installer('win32')
    else:
        print("ERROR: unsuported operating system")
        print("Check documentation for manual installation")
        sys.exit()

    ins.install(usrname, pswd, ACISS_path, shortcut_path, genome_path)


    
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
    #install(usrname, pswd, 'NewInstall', '/home/alister/Desktop', '/home/alister/Dropbox/BioInf/research/fakeGenome')


