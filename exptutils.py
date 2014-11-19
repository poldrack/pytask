"""
exptutils.py - utility functions for use with psychopy
"""

from psychopy import visual, core, event, logging,gui
import numpy as N
import pickle
import datetime
import sys
import os
from psychopy import visual, core, event, logging
import numpy as N
import pickle
import datetime
import sys
import os, socket
import inspect
import hashlib
from socket import gethostname
# general experimental routines

def store_scriptfile():
    scriptfile= inspect.getfile(inspect.currentframe())# save a copy of the script in the data file
    f=open(scriptfile)
    script=f.readlines()
    f.close()
    return script

def get_info_from_dialog(dictionary,title,fixed=[]):
    """ read in study information
    """
    infoDlg = gui.DlgFromDict(dictionary, title=title, fixed=fixed)
    if gui.OK:#then the user pressed OK
        print info
        return info
    else: 
        print 'User Cancelled'
        return []

def shut_down_cleanly(subdata,win):
    """
    shut down experiment and try to save data
    """
    
    win.close()
    logging.flush()
    try:
        f=open('Output/%s_%s_subdata.pkl'%(subdata['subcode'],subdata['datestamp']),'wb')
        pickle.dump(subdata,f)
        f.close()
    except:
        pass
#    if subdata['completed']==0:
#        sys.exit()
    
def md5Checksum(filePath):
    """ get an MD5 checksum for a file
    """
    # from http://www.joelverhagen.com/blog/2011/02/md5-hash-of-file-in-python/
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

def get_lists_from_directory(dir):
    """ find all files in a directory
    """
    if os.path.exists(dir):
        files_list=os.listdir(dir)
        files=[os.path.join(dir,f) for f in files_list]
    else:
        print '%s directory does not exist - exiting'%dir
        sys.exit()
    
    if files==[]:
        print '%s directory is empty'%dir
        #sys.exit()
        return []
    return files


def list_previously_used_stim(relative_stim_dir_name):
    current_dir=os.getcwd()
    stim_list_dir='%s/Output/stim_lists/%s'%(current_dir,relative_stim_dir_name)
#    os.chdir(stim_list_dir)
    used_stim=[]
    files_list=get_list_from_directory(stim_list_dir)
    for i in len(files_list):
        with open(files_list[1], 'r') as data:#name of data file
            reader = csv.reader((data.read()).split('\n'), delimiter=',')
        for row in reader:
            used_stim.append(row)
    return used_stim

#make relative_stim_dir_name within Output/stim_lists
