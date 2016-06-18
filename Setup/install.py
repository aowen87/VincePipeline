import sys
from linuxInstall import *


def install(usrname, pswd, ACISS_path, local_path):
    cur_os = sys.platform
    if cur_os.lower[:5] == 'linux' or cur_os.lower[:6] == 'darwin':
        linuxInstall(usrname, pswd, ACISS_path, local_path)    
    elif cur_os.lower[:5] == 'win32' or cur_ow.lower[:6] == 'cygwin':
        pass
    else:
        print("ERROR: unsuported operating system")
        print("Check documentation for manual installation")
        sys.exit()


if __name__ == "__main__":
    
