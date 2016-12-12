'''
pyocclient -- CLI interface

@author:     Florian Kaiser
@copyright:  2016 Max Planck Computing And Data Facility. All rights reserved.
@license:    MIT
@contact:    florian.kaiser@mpcdf.mpg.de
'''

import os
import sys
import math
import yaml
import locale
import argparse
import owncloud
import datetime


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

class Cli():
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="ownCloud CLI client",
            usage='''%s <command> [<args>]
Available commands are:
   init        Create template config file in user's homedirectory
   put         Upload file or directory to server
   get         Download file from server
   mkdir       Create directory on server
   list        List directory on server

The following environment variables need to be set:
   OC_SERVER   Address of the ownCloud server
               e.g. https://datashare.mpcdf.mpg.de
   OC_USER     ownCloud user
   OC_PASSWORD ownCloud password

Example:
   %s put /tmp/test.txt /remote_folder/
''' % (sys.argv[0], sys.argv[0]))
        parser.add_argument('command', help='Subcommand to run')

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        getattr(self, args.command)()

    """ Construct ownCloud client form environment variables"""
    def _client_from_environ(self):
        for var in ['OC_USER', 'OC_PASSWORD', 'OC_SERVER']:
            if not os.environ.has_key(var):
                raise CLIError("%s not set." % (var,))

        debug = os.environ.has_key('OC_DEBUG')

        client = owncloud.Client(os.environ['OC_SERVER'], debug=debug)
        client.login(os.environ['OC_USER'], os.environ['OC_PASSWORD'])

        return client


    """ Construct ownCloud client form environment variables"""
    def _client_from_config(self):

        for var in ['OC_USER', 'OC_PASSWORD', 'OC_SERVER']:
            if not os.environ.has_key(var):
                raise CLIError("%s not set." % (var,))
        debug = os.environ.has_key('OC_DEBUG')

        client = owncloud.Client(os.environ['OC_SERVER'], debug=debug)
        client.login(os.environ['OC_USER'], os.environ['OC_PASSWORD'])

        return client


    def _filesizeformat(self, value):
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
            raise ValueError("Number too big")
        else:
            scaled_value = round(float(value) / pow(_FILESIZE_BASE, suffix_index), 2)

        suffix = _FILESIZE_SUFFIXES[suffix_index]
        return "%g %s" % (scaled_value, suffix)

    def _print_file_list(self, l):
        file_info_str = lambda x: "{:6s} {:10s} {:18s} {:s}".format(x.file_type, self._filesizeformat(x.get_size()),
                                    x.get_last_modified().strftime('%x %X'), x.path)
        for x in l:
            print(file_info_str(x))

    def _get_timestamp():
        return '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())


    def init(self):
        config = {}
        config['OC_USER'] = "username"
        config['OC_SERVER'] = "https://datashare.mpcdf.mpg.de"
        config['OC_DEBUG'] = False


    # TODO: Progress indicator? Would need to hook into owncloud.__put_file_chunked...
    #   -> Or poor man's progress via DEUBG=1 printing HTTP request for each chunk
    # TODO: Support uploading multiple objects at the same time like cp?
    def put(self):
        parser = argparse.ArgumentParser(description='Upload file or directory to server')
        parser.add_argument('-r', '--recursive', action='store_true',
                            default=False, help='Recursively upload directory')
        parser.add_argument('source', help='Local source')
        parser.add_argument('destination', help='Remote destination')
        args = parser.parse_args(sys.argv[2:])

        client = self._client_from_environ()

        if os.path.isfile(args.source):
            client.put_file(args.destination, args.source)
        elif os.path.isdir(args.source):
            if not args.recursive:
                raise CLIError("Source is a directory, but recursive flag is not set.")
            else:
                client.put_directory(args.destination, args.source)
        elif not os.path.exists(args.source):
            raise CLIError("Source does not exist.")
        else:
            raise CLIError("Source is is not a normal file.")

        client.logout()


    def get(self):
        parser = argparse.ArgumentParser(description='Download file from remote server')
        parser.add_argument('source', help='Remote source')
        parser.add_argument('destination', help='Local destination')
        args = parser.parse_args(sys.argv[2:])

        client = self._client_from_environ()
        client.get_file(args.source, args.destination)
        client.logout()


    def mkdir(self):
        parser = argparse.ArgumentParser(description='Create directory on remote server')
        parser.add_argument('location', help='Remote location')
        args = parser.parse_args(sys.argv[2:])

        client = self._client_from_environ()
        client.mkdir(args.location)
        client.logout()


    def list(self):
        parser = argparse.ArgumentParser(description='List directory on the remote server')
        parser.add_argument('location', help='Remote location')
        args = parser.parse_args(sys.argv[2:])

        client = self._client_from_environ()

        l = client.list(args.location)
        self._print_file_list(l)

        client.logout()


# if __name__ == '__main__':
#     Cli()
