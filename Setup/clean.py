import argparse
import sys
import subprocess
import fileinput
import os
try:
    from paramiko import *
except ImportError:
    print("ERROR: manual installation of paramiko is required")

def rmShortcut(shortcut_path):
    """
       Remove the pipeline shortcut.
       param:
             shortcut_path: a string representation of the 
             shorcut path. 
    """
    print("Removing shortcut")
    subprocess.call(["rm", shortcut_path]) 

def removePaths(ACISS_path, osystem):
    """
       Remove all paths that were added to various files. These
       include the GUI files and PBS files. 
       param: 
             ACISS_path: string representation of the path to the
             ACISS repo. 
            osystem: string representation of the current os. 
    """
    print("Removing path insertions")
    if osystem == 'linux' or osystem == 'darwin':
        divider = '/'
    elif osystem == 'win32':
        divider = '\\'
    else:
        print("Invalid or unsuported os: ", osystem)
        sys.exit()

    gui_path   = ((divider).join(os.path.dirname(os.path.abspath(__file__)).split(divider)[:-1]) 
                   + "{}GUI{}".format(divider, divider))
    cache_path = gui_path + "__pycache__"
    if osystem == 'linux':
        Main_path  = gui_path + "Main.pyw"
        main_file  = open(Main_path).readlines()
        open(Main_path, 'w').writelines(main_file[1:])#FIXME: testing
    os.system("rm -r {}".format(cache_path))
    path_dirs = ['..{}PBS'.format(divider), '..{}GUI'.format(divider)]
    for path_dir in path_dirs:
        for root, dirs, files in os.walk(path_dir):
            for f in files:
                file_path = os.path.join(root, f)
                with fileinput.FileInput(file_path, inplace=True) as file:
                    for line in file:
                        print(line.replace(ACISS_path, '_PATH_INSERT_'), end='')     

def removeRemote(usrname, pswd, ACISS_path):
    """
       Remove the remote repo on ACISS. 
       param:
             usrname: string representation of the ACISS user name. 
             pswd: string representation of the ACISS password. 
             ACISS_path: string rep of the path to the ACISS repo. 
    """
    try:
        print("Attempting to connect to ACISS...")
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()
        client.connect('aciss.uoregon.edu', username=usrname, password=pswd)
        print("connected to ACISS!\nRemoving repo")
        command = 'rm -rf {}'.format(ACISS_path)
        stdin, stdout, stderr = client.exec_command(command)
        client.close()
    except Exception:
        pass


def fullClean(usrname, pswd, ACISS_path, shortcut_path, osystem):
    '''
       Uninstall program => remove ACISS repo, remove shortcut, 
       replace ACISS_path insertions with default. 
    '''
    removeRemote(usrname, pswd, ACISS_path)
    removePaths(ACISS_path, osystem)
    rmShortcut(shortcut_path)
    print("Uninstall complete")
    

if __name__ == "__main__":
    """
       For use with the command line. 
    """
    parser = argparse.ArgumentParser("Remove install")
    parser.add_argument('usrname', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('ACISS_path', type=str)
    parser.add_argument('shortcut_path', type=str)
    parser.add_argument('osystem', type=str)
    args          = parser.parse_args()
    usrname       = args.usrname
    pswd          = args.password
    ACISS_path    = args.ACISS_path
    shortcut_path = args.shortcut_path
    osystem       = args.osystem
    Fullclean(usrname, pswd, ACISS_path, shortcut_path, osystem)
