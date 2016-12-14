Python OwnCloud Client (poc), minimal version
=============================================

Copyright (c) 2016, 2017 Florian Kaiser, fek@rzg.mpg.de
                           Klaus Reuter, khr@rzg.mpg.de


requirements and installation
-----------------------------

As a requirement, poc needs the official OwnCloud Python module installed.

`pip install --user pyocclient`


basic functionality (optional arguments in parentheses)
-------------------------------------------------------

* upload single file

  `poc put local_file_name`

* download single file

  `poc get remote_file_name`

* list remote files and folders

  `poc ls (remote_folder)`

* create remote directory

  `poc mkdir remote_folder`

* initialize configuration, create "~/.pocrc"

* check if configuration actually works

  `poc checkconfig`


under the hood
--------------

In any case a client (== connection) needs to be created.  This requires a valid
configuration.  The configuration file is located at "~/.pocrc".
No credentials are ever stored in "~/.pocrc".


credentials and security considerations
---------------------------------------

Security concerns arise, because often, the OwnCloud password is identical to
the password used for other services at a site.

The environment variable OC_PASSWORD may be set to a valid password, for security
reasons using the `pocpasswd` bash function from `pocpasswd.sh` in order to
prevent the plain text password from showing up in the shell history.  Support
for other shells may follow later.  When using OC_PASSWORD close the shell as
soon as possible after the file transfer operations have been done.

In case the environment variable OC_PASSWORD is not set the `poc` command asks
for the password at every invocation.
