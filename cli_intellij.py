# coding:utf-8

import cli_common
import os
import getpass


class IntellijCli(object):
    """
    管理intellij cli程序，OS support: ubuntu
    """

    def install(self):
        """
        安装intellij

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        varHostSshIp = ""
        varHostSshUser = ""
        varHostSshPassword = ""
        varSudoPassword = ""
        varInstallLocally = "n"

        var_install = input("安装intellij吗? [y/n]: ")
        if var_install.lower() == "y":
            varInstallLocally = input("是否本地安装？ [y/n]: ") or "n"
            if not varInstallLocally == "y":
                varHostSshIp = input("安装主机（例如： 192.168.1.20:8080）：")
                varHostSshUser = input("安装主机的SSH用户（默认 root）：") or "root"
                varHostSshPassword = getpass.getpass("输入SSH密码：")

            varSudoPassword = getpass.getpass("输入sudo密码，如果当前为root用户不需要输入：")

        if var_install.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_intellij_install.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                    varHostSshPassword, varSudoPassword,
                                                    varInstallLocally.lower() == "y")

            cli_common.execute_command(var_command)
