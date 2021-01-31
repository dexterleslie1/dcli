# dcli
A cli tool named dcli to make work more handy, Support OS: centOS8

Use curl to download setup.sh
curl --proxy socks5h://host:port https://raw.githubusercontent.com/dexterleslie1/dcli/master/setup.sh --output /tmp/setup.sh

shell scripting styleguide refer to https://zh-google-styleguide.readthedocs.io/en/latest/google-shell-styleguide/contents/#shell

Examples:

# Install openresty from source code
dcli openresty --from-source true

# Install openresty from binary packages
dcli openresty --from-source false


