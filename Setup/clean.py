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
    print("Removing shortcut")
    subprocess.call(["rm", shortcut_path]) 

def removePaths(ACISS_path, osystem):
    print("Removing path insertions")
    if osystem == 'linux' or osystem == 'darwin':
        divider = '/'
    elif osystem == 'win32':
        divider = '\\'
    else:
        print("Invalid or unsuported os: ", osystem)
        sys.exit()
    cache_path = ((divider).join(os.path.dirname(os.path.abspath(__file__)).split(divider)[:-1]) 
                 + "{}GUI{}__pycache__".format(divider, divider))
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
