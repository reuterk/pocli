# Helper function to allow to set the password for poc as environment variable
# without having it appear in bash history.
# Source ("source") this file into your bash session and then call the function.

function pocpasswd() {
    echo -n " Enter your OwnCloud password (will not be echoed/visible): "
    read -s PASSWORD
    echo
    export OC_PASSWORD="$PASSWORD"
}
