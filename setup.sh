#!/bin/bash

#
# Shell for setup dcli
# 支持操作系统：ubuntu20、centOS7、centOS8
# NOTE：centOS6从python2.6升级到python2.7之后，pip install fire无法正常工作

########################
# 解决centOS eol问题
# 参考 https://stackoverflow.com/questions/70926799/centos-through-vm-no-urls-in-mirrorlist
########################
setup_resolve_centOS_eol() {
    varUname=`uname -a`
    # 转换为小写
    varUname=${varUname,,}

    # 当centOS8时
    if [[ $varUname =~ "el8" ]]; then
        sed -i 's/^mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
        sed -i 's|^#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
    fi
}

########################
# Install git cli
########################
setup_install_git_cli() {
  # Check if git cli install
  which git &>/dev/null
  if [ $? -eq 1 ]; then
    varUname=`uname -a`
    # 转换为小写
    varUname=${varUname,,}
 
    # When centOS7
    if [[ $varUname =~ "el7" ]]; then
     echo "Detecting git cli is not installed, Installing please wait..."
     yum -y install https://packages.endpoint.com/rhel/7/os/x86_64/endpoint-repo-1.7-1.x86_64.rpm &> /dev/null
    fi

    varCentOS="el"
    varUbuntu="ubuntu"
    if [[ $varUname =~ $varCentOS ]]; then
        yum install -y git
    elif [[ $varUname =~ $varUbuntu ]]; then
        sudo apt-get install git -y
    fi
  else
    echo "Git cli is installed already"
  fi
}

########################
# Setup dcli
########################
setup_dcli() {
 # Remove *.pyc
 sudo rm -rf /usr/bin/dcli-env/*.pyc

 # 关闭ssl验证，否则git命令会抛出关于自签名证书错误
 git config --global http.sslVerify false

 # Clone dcli repository if not exists
 if [ ! -d "/tmp/dcli" ]; then
  git clone https://github.118899.net/dexterleslie1/dcli.git /tmp/dcli
 else
  ( cd /tmp/dcli && git pull )
 fi

# # 恢复ssl验证
# git config --global http.sslVerify true

 sudo rm -rf /usr/bin/dcli-env
 sudo cp -r /tmp/dcli /usr/bin/dcli-env
 if [ ! -f /usr/bin/dcli ]; then
  sudo ln -s /usr/bin/dcli-env/dcli.py /usr/bin/dcli
 fi
 sudo chmod +x /usr/bin/dcli
}

########################
# Setup ansible
########################
setup_ansible() {
  # 判断操作系统类型执行相应的命令按照ansible
  # 目前只支持centOS和ubuntu
  varUname=`uname -a`
  # 转换为小写
  varUname=${varUname,,}
  varCentOS="el"
  varUbuntu="ubuntu"
  if [[ $varUname =~ $varCentOS ]]; then
      yum -y install epel-release
      yum -y install ansible
  elif [[ $varUname =~ $varUbuntu ]]; then
      # sudo apt-get install software-properties-common
      sudo apt-add-repository ppa:ansible/ansible -y
      sudo apt-get update
      sudo apt-get install ansible -y
  else
      echo "setup.sh程序目前只支持centOS和ubuntu操作系统"
      exit
  fi

  # 非ubuntu系统才配置mitogen ansible插件
  if ! [[ $varUname =~ $varUbuntu ]]; then
    # 判断/etc/ansible/ansible.cfg文件是否存在[defaults]，否则追加
    sudo grep -q '^\[defaults\]' /etc/ansible/ansible.cfg
    if ! [[ $? -eq 0 ]]; then
      echo "[defaults]" | sudo tee -a /etc/ansible/ansible.cfg 1>/dev/null
    fi

    # 配置ansible mitogen插件
    sudo grep -q '^strategy_plugins =' /etc/ansible/ansible.cfg
    if [[ $? -eq 0 ]]; then
      sudo sed -i 's/^strategy_plugins =.*$/strategy_plugins = \/usr\/bin\/dcli-env\/mitogen-0.2.10-rc.0\/ansible_mitogen\/plugins\/strategy/' /etc/ansible/ansible.cfg
    else
      sudo sed -i '/^\[defaults\]/a strategy_plugins = \/usr\/bin\/dcli-env\/mitogen-0.2.10-rc.0\/ansible_mitogen\/plugins\/strategy' /etc/ansible/ansible.cfg
    fi

    sudo grep -q '^strategy =' /etc/ansible/ansible.cfg
    if [[ $? -eq 0 ]]; then
      sudo sed -i 's/^strategy =.*$/strategy = mitogen_linear/' /etc/ansible/ansible.cfg
    else
      sudo sed -i '/^\[defaults\]/a strategy = mitogen_linear' /etc/ansible/ansible.cfg
    fi
  fi
}

########################
# Setup python
########################
setup_python() {
  varUname=`uname -a`
  # 转换为小写
  varUname=${varUname,,}
  varCentOS="el"
  varUbuntu="ubuntu"
  if [[ $varUname =~ $varCentOS ]]; then
      yum -y install epel-release
      # centOS8安装python3
      yum -y install python3-pip
  elif [[ $varUname =~ $varUbuntu ]]; then
      sudo apt-get install python3-pip -y
      pip3 install setuptools
  fi

  pip3 install fire
  pip3 install enquiries
}

########################
# Main
########################
main() {
  setup_resolve_centOS_eol
  setup_ansible
  setup_install_git_cli
  setup_python
  setup_dcli
}

main
