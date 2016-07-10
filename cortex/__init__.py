'''Setup scripts for Cortex.

'''

import readline, glob
from os import path
import urllib2

from .datasets import fetch_basic_data
from .datasets.neuroimaging import fetch_neuroimaging_data
from .models import get_cell_manager
from .utils.tools import get_paths
from .utils.extra import (
    complete_path, query_yes_no, write_default_theanorc, write_path_conf)


cell_manager = get_cell_manager()

def main():
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind('tab: complete')
    readline.set_completer(complete_path)
    print ('Welcome to Cortex: a deep learning toolbox for '
            'neuroimaging')
    print ('Cortex requires that you enter some paths for '
            'default dataset and output directories. These '
            'can be changed at any time and are customizable '
            'via the ~/.cortexrc file.')

    try:
        path_dict = get_paths()
    except ValueError:
        path_dict = dict()

    if '$data' in path_dict:
        data_path = raw_input(
            'Default data path: [%s] ' % path_dict['$data']) or path_dict['$data']
    else:
        data_path = raw_input('Default data path: ')
    data_path = path.expanduser(data_path)
    if not path.isdir(data_path):
        raise ValueError('path %s does not exist. Please create it.' % data_path)

    if '$outs' in path_dict:
        out_path = raw_input(
            'Default output path: [%s] ' % path_dict['$outs']) or path_dict['$outs']
    else:
        out_path = raw_input('Default output path: ')
    out_path = path.expanduser(out_path)
    if not path.isdir(out_path):
        raise ValueError('path %s does not exist. Please create it.' % out_path)
    write_path_conf(data_path, out_path)

    print ('Cortex demos require additional data that is not necessary for '
           'general use of the Cortex as a package.'
           'This includes MNIST, Caltech Silhoettes, and some UCI dataset '
           'samples.')

    answer = query_yes_no('Download basic dataset? ')

    if answer:
        try:
            fetch_basic_data()
        except urllib2.HTTPError:
            print 'Error: basic dataset not found.'

    print ('Cortex also requires neuroimaging data for the neuroimaging data '
           'for the neuroimaging demos. These are large and can be skipped.')

    answer = query_yes_no('Download neuroimaging dataset? ')

    if answer:
        try:
            fetch_neuroimaging_data()
        except urllib2.HTTPError:
            print 'Error: neuroimaging dataset not found.'

    home = path.expanduser('~')
    trc = path.join(home, '.theanorc')
    if not path.isfile(trc):
        print 'No %s found, adding' % trc
        write_default_theanorc()