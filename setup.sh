#!/bin/bash
#
# Shell for setup automation environment

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
# Setup automation environment
########################
setup_automation_environment() {
 # Clone automation-scripting repository if not exists
 if [ ! -d "/usr/local/automation-scripting" ]; then
  git clone https://github.com/dexterleslie1/automation-scripting.git /usr/local/automation-scripting
 fi
}

########################
# Main
########################
main() {
 setup_install_git_cli
 setup_automation_environment
}

main
