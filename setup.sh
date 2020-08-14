#!/bin/bash
#
# Shell for setup dcli

########################
# Install git cli
########################
setup_install_git_cli() {
 # Check if git cli install
 which git &>/dev/null
 VAR_RESULT=$?
 if [ $VAR_RESULT -eq 1 ]; then
  VAR_OS_VERSION=`uname -a`
 
  # When centOS7
  if [[ "$VAR_OS_VERSION" =~ "el7" ]]; then
   echo "Detecting git cli is not installed, Installing please wait..."
   yum -y install https://packages.endpoint.com/rhel/7/os/x86_64/endpoint-repo-1.7-1.x86_64.rpm &> /dev/null
  fi
  yum install -y git
 else
  echo "Git cli is installed already"
 fi
}

########################
# Setup dcli
########################
setup_dcli() {
 # Clone dcli repository if not exists
 if [ ! -d "/tmp/dcli" ]; then
  git clone https://github.com/dexterleslie1/dcli.git /tmp/dcli
 else
  ( cd /tmp/dcli && git pull )
 fi
 
 cp -r /tmp/dcli /usr/bin/dcli-env
 if [ ! -f /usr/bin/dcli ]; then
  ln -s /usr/bin/dcli-env/dcli.py /usr/bin/dcli
 fi
 chmod +x /usr/bin/dcli
}

########################
# Setup ansible
########################
setup_ansible() {
  yum -y install epel-release
  yum -y install ansible
}

########################
# Main
########################
main() {
  setup_ansible
  setup_install_git_cli
  setup_dcli
}

main