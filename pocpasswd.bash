# Helper function to allow to set the password for poc as environment variable
# without having it appear in bash history.  Source ("source pocpasswd.bash")
# this file into your bash session, and call `pocpasswd`.

function pocpasswd() {
    echo -n "OwnCloud password (will not be echoed/visible): "
    read -s PASSWORD
    echo
    export OC_PASSWORD="$PASSWORD"
}
