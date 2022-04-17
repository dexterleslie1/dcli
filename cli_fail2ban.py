# coding:utf-8

import cli_common
import os
import getpass


class Fail2banCli(object):
    """
    fail2ban管理工具。 支持操作系统: centOS8
    """

    def install(self):
        """
        安装fail2ban

        :return:
        """

        varHostSshIp = ""
        varHostSshUser = ""
        varHostSshPassword = ""
        varSudoPassword = ""
        varInstallLocally = "n"

        varInstall = input("是否安装fail2ban？ [y/n]: ") or "n"
        if varInstall.lower() == "y":
            varInstallLocally = input("是否本地安装？ [y/n]: ") or "n"
            if not varInstallLocally == "y":
                varHostSshIp = input("安装主机（例如： 192.168.1.20:8080）：")
                varHostSshUser = input("安装主机的SSH用户（默认 root）：") or "root"
                varHostSshPassword = getpass.getpass("输入SSH密码：")

            varSudoPassword = getpass.getpass("输入sudo密码，如果当前为root用户不需要输入：")

        if varInstall.lower() == "y":
            varFullPath = os.path.dirname(os.path.realpath(__file__))
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_fail2ban_install.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                    varHostSshPassword, varSudoPassword, varInstallLocally.lower() == "y")
            var_command = var_command + " -e varFrontend=true"
            cli_common.execute_command(var_command)