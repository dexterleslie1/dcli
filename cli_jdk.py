# coding:utf-8

import cli_common
import os
import getpass


class JdkCli(object):
    """
    管理jdk。 支持的系统: centOS、debian10、ubuntu
    """

    def install(self):
        """
        安装jdk

        :return:
        """

        varInstallJdk = input("是否安装jdk？ [y/n]: ") or "n"

        if varInstallJdk.lower() == "y":

            varHostSshIp = ""
            varHostSshUser = ""
            varHostSshPassword = ""
            varSudoPassword = ""

            varInstallLocally = input("是否本地安装？ [y/n]: ") or "n"
            if not varInstallLocally == "y":
                varHostSshIp = input("输入目标主机（例如： 192.168.1.20:8080）：")
                varHostSshUser = input("输入目标主机SSH用户（默认 root）：") or "root"
                varHostSshPassword = getpass.getpass("输入SSH密码：")

            varSudoPassword = getpass.getpass("输入主机的sudo密码，如果当前为root用户不需要输入：")

            varFullPath = os.path.dirname(os.path.realpath(__file__))

            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_jdk_install.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                    varHostSshPassword, varSudoPassword, varInstallLocally.lower() == "y")
            cli_common.execute_command(var_command)