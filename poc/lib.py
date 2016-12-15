"""poc library and basic methods

Initial version based on "pyocclient.py" by Florian Kaiser.
"""


import os
import sys
import math
#import yaml
import json
import time
import locale
import argparse
import owncloud
import datetime
import getpass


__version__ = 0.1


class CLIError(Exception):
    '''Generic CLIError to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg


def _get_timestamp():
    return '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())


def _get_pocrc():
    home = os.path.expanduser('~')
    rcfile = os.path.join(home, '.pocrc')
    return rcfile


"""Construct ownCloud client based on the configuration file."""
def _client():
    if 'OC_PASSWORD' in os.environ:
        password = os.environ['OC_PASSWORD']
    else:
        password = getpass.getpass()
    config = {}
    rcfile = _get_pocrc()
    with open(rcfile, 'r') as fp:
        #config = yaml.load(fp)
        config = json.loads( fp.read() )
    config['OC_PASSWORD'] = password
    client = owncloud.Client(config['OC_SERVER'], debug=config['OC_DEBUG'])
    client.login(config['OC_USER'], config['OC_PASSWORD'])
    return client


def _filesizeformat(value):
    """
    Converts an integer representing the size of a file-like object
    in bytes into human readable form (i.e. 13 KB, 4.1 MB, etc).
    """
    _FILESIZE_BASE = 1024
    _FILESIZE_SUFFIXES = ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z')
    if value is None or value == "":
        return ""
    if type(value) != int:
        try:
            value = float(value)
        except:
            return ""
    suffix_index = 0 if value==0 else int(math.log(value) / math.log(_FILESIZE_BASE))
    if suffix_index == 0:
        scaled_value = value
    elif suffix_index > len(_FILESIZE_SUFFIXES)-1:
        raise ValueError("number too big")
    else:
        scaled_value = round(float(value) / pow(_FILESIZE_BASE, suffix_index), 2)
    suffix = _FILESIZE_SUFFIXES[suffix_index]
    return "%g %s" % (scaled_value, suffix)


def _print_file_list(l):
    file_info_str = lambda x: "{:6s} {:10s} {:18s} {:s}".format(x.file_type, _filesizeformat(x.get_size()),
                                x.get_last_modified().strftime('%x %X'), x.path)
    for x in l:
        print(file_info_str(x))


def _init_pocrc():
    config = {}
    config['OC_USER'] = getpass.getuser()
    config['OC_SERVER'] = "https://datashare.mpcdf.mpg.de"
    config['OC_DEBUG'] = False
    rcfile = _get_pocrc()
    with open(rcfile, 'w') as fp:
        #yaml.dump(config, fp, default_flow_style=False)
        fp.write( json.dumps(config, sort_keys=True, indent=4, separators=(',', ': ')) )
    print("created config file: " + rcfile)


# --- routines called by the cli interface (cli.py) below ---


def put(argparse_args):
    if (argparse_args.destination):
        destination = argparse_args.destination
    else:
        destination = '/'
    args = vars(argparse_args)
    file_list = args['files']
    if (len(file_list) > 0):
        client = _client()
        try:
            lst = client.list(destination)
        except:
            print("remote directory \"%s\" is not accessible" % destination)
        else:
            for file in file_list:
                if os.path.isfile(file):
                    size_mb = float(os.path.getsize(file))/float(1024*1024)
                    file_basename = os.path.basename(file)
                    if (size_mb > 100.0):
                        print("%s : large file detected (%.2f MB), transfer may take some time ..." % (file_basename, size_mb))
                    t0 = time.time()
                    client.put_file(os.path.join(destination, file_basename), file)
                    t1 = time.time()
                    dt = t1 - t0
                    print("%s : OK (%.2f MB/s)" % (file_basename, size_mb/dt))
                else:
                    print("%s is not a regular file" % file)
        client.logout()
    else:
        print("nothing to do")


def get(argparse_args):
    if (argparse_args.destination):
        destination = argparse_args.destination
    else:
        destination = '.'
    args = vars(argparse_args)
    file_list = args['files']
    if os.path.isdir(destination):
        client = _client()
        for file in file_list:
            file_basename = os.path.basename(file)
            file_target = os.path.join(destination, file_basename)
            t0 = time.time()
            client.get_file(file, file_target)
            t1 = time.time()
            dt = t1 - t0
            size_mb = float(os.path.getsize(file_target))/float(1024*1024)
            print("%s : OK (%.2f MB/s)" % (file_basename, size_mb/dt))
        client.logout()
    else:
        print("invalid destination")


def ls(argparse_args):
    args = vars(argparse_args)
    directory_list = args['dir']
    if (len(directory_list) == 0):
        directory_list.append('/')
    client = _client()
    for dir in directory_list:
        try:
            lst = client.list(dir)
        except:
            print("remote directory \"%s\" is not accessible" % dir)
        else:
            _print_file_list(lst)
    client.logout()


def mkdir(argparse_args):
    args = vars(argparse_args)
    directory_list = args['dir']
    if (len(directory_list) > 0):
        client = _client()
        for dir in directory_list:
            client.mkdir(dir)
        client.logout()
    else:
        print("nothing to do")


def check(argparse_args):
    try:
        _client()
    except:
        raise
    else:
        print("OK!")


def init(argparse_args):
    _init_pocrc()
