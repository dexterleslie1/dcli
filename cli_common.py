import subprocess
import logging
import getpass
import os


def prompt(component=None, install=None, target_host=None, target_host_user='root', target_host_password=None,
           sudo_password=None, ansible_role_file=None):
    # 无人值守安装
    unattended_intall = install and install.strip() == "y"

    if not unattended_intall:
        install = input("是否安装和配置" + component + "？ [y/n]：") or "n"

    if install.lower() == "y":

        if not unattended_intall:
            install_locally = input("是否本地安装？ [y/n]: ") or "n"
        else:
            install_locally = "y" if not target_host or not target_host.strip() else "n"

        if not unattended_intall and not install_locally == "y":
            target_host = input("目标主机（例如： 192.168.1.20:8080）：")
            target_host_user = input("目标主机SSH用户（默认 root）：") or "root"
            target_host_password = getpass.getpass("输入SSH密码：")

        if not unattended_intall:
            sudo_password = getpass.getpass("输入主机的sudo密码，如果当前为root用户不需要输入：")

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/" + ansible_role_file
        var_command = concat_command(var_command, target_host, target_host_user
                                     , target_host_password, sudo_password,
                                     install_locally.lower() == "y", unattended_intall)
    else:
        var_command = ""
        install_locally = "n"

    # 是否本地安装，否则完成安装后重启服务器
    var_command = var_command + " -e \"install_locally=" + str(install_locally.lower() == "y") + "\""

    return unattended_intall, var_command, install


def execute_command(command):
    logging.info("Prepare to execute command '" + command + "'")
    var_result = subprocess.call(command, shell=True)
    if var_result != 0:
        raise Exception("Run command '" + command + "' failed")


def execute_command_by_subprocess_run(command, isLogging=False):
    if isLogging:
        logging.info("Prepare to execute command '" + command + "'")
    varResult = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               encoding="utf-8")
    # varStdErr = varResult.stderr
    # if varStdErr is not None and len(varStdErr.strip()) != 0:
    #     raise Exception("执行命令 '" + command + "' 失败，原因如下：\n" + varStdErr )
    return varResult


def concat_command(command, remote_hosts, remote_user, remotePassword=None, sudoPassword=None, installLocally=False,
                   unattended_intall=False):
    if remotePassword is None:
        if remote_hosts:
            if not remote_hosts.endswith(","):
                remote_hosts = remote_hosts + ","
            command = command + " --inventory " + remote_hosts
        if remote_user:
            command = command + " --user " + remote_user

        if not unattended_intall:
            command = command + " --ask-pass"
    else:
        if remote_hosts:
            if not remote_hosts.endswith(","):
                remote_hosts = remote_hosts + ","
            command = command + " --inventory " + remote_hosts
        if remote_user:
            command = command + " --user " + remote_user

        # https://stackoverflow.com/questions/41771725/ansible-2-1-2-playbook-pass-ssh-password-and-sudo-password-as-command-line-args
        # command = command + "-e \"ansible_user=username ansible_ssh_pass=xxx ansible_sudo_pass=xxx\""
        command = command + " -e \"ansible_ssh_pass=" + remotePassword + "\""

    if sudoPassword is not None:
        command = command + " -e \"ansible_sudo_pass=" + sudoPassword + "\""

    if installLocally:
        command = command + " --connection=local -i 127.0.0.1,"

    return command
