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
 # Remove *.pyc
 rm -rf /usr/bin/dcli-env/*.pyc

 # Clone dcli repository if not exists
 if [ ! -d "/tmp/dcli" ]; then
  git clone https://github.118899.net/dexterleslie1/dcli.git /tmp/dcli
 else
  ( cd /tmp/dcli && git pull )
 fi

 rm -rf /usr/bin/dcli-env
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

  # 配置ansible mitogen插件
  grep -q '^strategy_plugins =' /etc/ansible/ansible.cfg
  if [[ $? -eq 0 ]]; then
    sed -i 's/^strategy_plugins =.*$/strategy_plugins = \/usr\/bin\/dcli-env\/mitogen-0.2.10-rc.0\/ansible_mitogen\/plugins\/strategy/' /etc/ansible/ansible.cfg
  else
    sed -i '/^\[defaults\]/a strategy_plugins = \/usr\/bin\/dcli-env\/mitogen-0.2.10-rc.0\/ansible_mitogen\/plugins\/strategy' /etc/ansible/ansible.cfg
  fi

  grep -q '^strategy =' /etc/ansible/ansible.cfg
  if [[ $? -eq 0 ]]; then
    sed -i 's/^strategy =.*$/strategy = mitogen_linear/' /etc/ansible/ansible.cfg
  else
    sed -i '/^\[defaults\]/a strategy = mitogen_linear' /etc/ansible/ansible.cfg
  fi
}

########################
# Setup python
########################
setup_python() {
  yum -y install epel-release
  yum -y install python2-pip
  pip2 install fire
}

########################
# Main
########################
main() {
  setup_ansible
  setup_install_git_cli
  setup_python
  setup_dcli
}

main