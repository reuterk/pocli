# Helper function to allow to set the password for `oc` as environment variable
# without having it appear in bash history.  Source ("source ocpasswd.bash")
# this file into your bash session, and call `ocpasswd`.

function ocpasswd() {
    echo -n "OwnCloud password (will not be echoed/visible): "
    read -s PASSWORD
    echo
    export OC_PASSWORD="$PASSWORD"
}
