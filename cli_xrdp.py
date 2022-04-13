# coding:utf-8

import cli_common
import os
import getpass


class XrdpCli(object):
    """
    xrdp管理工具。 支持操作系统： centOS8、ubuntu
    """

    def install(self):
        """
        安装xrdp

        :return:
        """

        # Full path of python file locates in
        varFullPath = os.path.dirname(os.path.realpath(__file__))

        varHostSshIp = ""
        varHostSshUser = "root"
        varHostSshPassword = ""
        varInstallLocally = "n"
        varSudoPassword = ""

        varInstall = input("安装xrdp？ [y/n]: ")
        if varInstall.lower() == "y":
            varInstallLocally = input("是否本地安装xrdp？ [y/n]: ") or "n"
            if not varInstallLocally == "y":
                varHostSshIp = input("请输入目标主机ip地址（例如： 192.168.1.20:8080）： ")
                varHostSshUser = input("请输入目标主机登录用户（默认： root）： ") or "root"
                varHostSshPassword = getpass.getpass("输入SSH密码：")

            varSudoPassword = getpass.getpass("输入sudo密码，如果当前为root用户不需要输入：")

        if varInstall.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_xrdp_install.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                    varHostSshPassword, varSudoPassword,
                                                    varInstallLocally.lower() == "y")
            cli_common.execute_command(var_command)