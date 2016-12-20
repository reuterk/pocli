Python OwnCloud Client (pocli)
==============================


Copyright (c) 2016, 2017
Florian Kaiser (fek@rzg.mpg.de), Klaus Reuter (khr@rzg.mpg.de)


Introduction
------------

The pocli package provides a lightweight OwnCloud command line client for basic
file operations such as upload, download, directory creation and listing, and
deletion.  It is built upon the official pyocclient package.


Requirements and installation
-----------------------------

pocli was developed and tested with Python 2.7.12 and Python 3.5.2.

As a requirement, pocli needs the official OwnCloud Python module:

`pip install --user pyocclient`

The pocli package itself can be installed in the standard way:

`python setup.py install --user`

Make sure to add the installation directory to the PATH environment variable,
on a Unix system this is for example "~/.local/bin".  The previous examples
pass the "--user" flag in order to work purely in the user's homedirectory.  In
case this flag is omitted, system-wide locations are chosen.


Functionality examples (optional arguments are given in parentheses)
--------------------------------------------------------------------

The pocli package provides the single `oc` command.  It takes positional and
named arguments in analogy to `git`.  The following examples illustrate the
basic usage:

* basic help

  `oc --help`

* command-specific help

  `oc command --help`

* list remote files and folders, defaults to "/"

  `oc ls <remote_folder>`

* create remote directory "temp"

  `oc mkdir temp`

* upload single file to the OwnCloud root directory

  `oc put file1`

* upload multiple files to the OwnCloud "temp" directory

  `oc put --directory=temp file1 file2 file3`

* download single file from OwnCloud to the current working directory

  `oc get file1`

* download multiple files to the local "temp" directory

  `oc get --directory=temp file1 file2 file3`

* remove remote file(s)

  `oc rm file1 file2`

* check if a connection to the server can be established successfully based on the present configuration

  `oc check`



Under the hood
--------------

The connection to an OwnCloud instance requires a valid configuration. The
configuration file in JSON format is located at "~/.pocrc" and created at the
first invocation of the `oc` command. The default configuration is for the
MPCDF datashare service, however, it can be configured freely to connect to
other OwnCloud instances.  No credentials are ever stored in "~/.pocrc".


Credentials and security considerations
---------------------------------------

Security concerns arise, in particular if the OwnCloud password is identical to
the password used for other services at the same site.

The environment variable OC\_PASSWORD may be set to a valid password, for
security reasons using the `ocpasswd` bash function from `ocpasswd.sh` in
order to prevent the plain text password from showing up in the shell history.
Execute the commands `source ocpasswd.bash`  followed by `ocpasswd`.  Support
for other shells may follow later.  When using OC\_PASSWORD, unset it or close
the shell as soon as possible after the file transfer operations have been
done.

In case the environment variable OC\_PASSWORD is not set the `oc` command asks
for the password at every invocation.
