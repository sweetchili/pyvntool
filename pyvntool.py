#!/usr/bin/python

import sys
import subprocess
import argparse
from pipes import quote

def format_file_list(output):
    files = ''
    
    while True:
        file = output.stdout.readline()
        if not file: break;
        
        file = file.replace('\n', '')
        if '@' in file:
            file += '@'
        files += ' %s' % file
    return files
    

class AddAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        output = subprocess.Popen("svn status %s | grep ^? | awk '{print $2}'" % quote(value), shell=True, stdout=subprocess.PIPE)
        files = format_file_list(output)
        
        if not files: return
        
        add = subprocess.Popen('svn add %s' % files, shell=True)
        print add.communicate()
        
class NewAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        output = subprocess.Popen('svn status %s | grep "^?" | awk "{print $2}"' % quote(value), shell=True)
        print output.communicate()

class ChangedAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        output = subprocess.Popen("svn status %s | grep ^M | awk '{print $2}'" % quote(value), shell=True)
        print output.communicate()

class DiffAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        output = subprocess.Popen("svn status %s | grep ^M | awk '{print $2}' | xargs svn diff | colordiff" % quote(value), shell=True)
        print output.communicate()

class CommitAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        output = subprocess.Popen("svn status %s | grep '^A\|^M' | awk '{print $2}'" % quote(value), shell=True, stdout=subprocess.PIPE)
        files_to_commit = format_file_list(output)
        commit_msg = raw_input('commit message: ')
        command = 'svn commit {0} -m "{1}"'.format(files_to_commit, commit_msg)
        commit = subprocess.Popen(command, shell=True,) 
        print commit.communicate()

if __name__ == "__main__":
    currentdir = "."
    
    parser = argparse.ArgumentParser(description="Ease the use of version control")
    parser.add_argument('-a', action=AddAction, help="add all files in the current or given directory", nargs='?', const=currentdir, type=str)
    parser.add_argument('-n', action=NewAction, help='list all new files in the current or given directory', nargs='?', const=currentdir, type=str)
    parser.add_argument('-ls', action=ChangedAction, help='list all change files in the current or given directory', nargs='?', const=currentdir, type=str)
    parser.add_argument('-d', action=DiffAction, help='diff all files in the current or given directory', nargs='?', const=currentdir, type=str)
    parser.add_argument('-c', action=CommitAction, help='commit all files in the current or given directory. asking for commit message', nargs='?', const=currentdir, type=str)
    
    if not len(sys.argv[1:]) == 0:
        parser.parse_args(sys.argv[1:])
    else:
        parser.print_help()
	
    
