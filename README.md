Python OwnCloud Client (poc)
============================

Copyright (c) 2016, 2017 Florian Kaiser, fek@rzg.mpg.de
                           Klaus Reuter, khr@rzg.mpg.de


Requirements and installation
-----------------------------

As a requirement, poc needs the official OwnCloud Python module installed:

`pip install --user pyocclient`

The poc package itself can be installed in the standard way:

`python setup.py install --user`

Make sure to add the installation directory to the PATH environment variable,
on a Unix system this is for example "~/.local/bin".  The previous examples
passed the "--user" flag in order to work purely in the user's homedirectory.
In case this flag is omitted, system-wide locations are chosen if the
permissions allow this.


Functionality examples (optional arguments are given in parentheses)
--------------------------------------------------------------------


* basic help

  `poc --help`

* command specific help

  `poc command --help`

* initialize configuration, create "~/.pocrc", defaulting to MPCDF

  `poc init`

* check if the configuration actually works

  `poc check`

* list remote files and folders, defaults to "/"

  `poc ls (remote_folder)`

* create remote directory "temp"

  `poc mkdir temp`

* upload single file to OwnCloud root directory

  `poc put file1`

* upload multiple files to OwnCloud "temp" directory

  `poc put --destination=temp file1 file2 file3`

* download single file from OwnCloud directory to the current working directory

  `poc get file1`

* download multiple files to the local "temp" directory

  `poc get --destination=temp file1 file2 file3`



Under the hood
--------------

In any case a client (== connection) needs to be created.  This requires a valid
configuration.  The configuration file is located at "~/.pocrc".
No credentials are ever stored in "~/.pocrc".


Credentials and security considerations
---------------------------------------

Security concerns arise, in particular if the OwnCloud password is identical to
the password used for other services at a site.

The environment variable OC_PASSWORD may be set to a valid password, for security
reasons using the `pocpasswd` bash function from `pocpasswd.sh` in order to
prevent the plain text password from showing up in the shell history.  Support
for other shells may follow later.  When using OC_PASSWORD, close the shell as
soon as possible after the file transfer operations have been done.
Execute the commands `source pocpasswd.bash`  followed by `pocpasswd`.


In case the environment variable OC_PASSWORD is not set the `poc` command asks
for the password at every invocation.
