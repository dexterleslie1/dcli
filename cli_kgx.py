import cli_common
import os
import getpass
import logging


class KgxCli(object):
    """
    kgx管理工具。配置kgx crond重启任务。支持操作系统： centOS8
    """

    def install(self):
        """
        安装kgx

        :return:
        """

        # Full path of python file locates in
        varFullPath = os.path.dirname(os.path.realpath(__file__))

        varInstall = input("是否安装kgx？ [y/n]： ")
        varInstallLocally = "n"

        varHostSshIp = None
        varHostSshUser = None
        varHostSshPassword = ""
        varSudoPassword = ""

        if varInstall.lower() == "y":
            varInstallLocally = input("是否本地安装kgx？ [y/n]: ") or "n"
            if not varInstallLocally == "y":
                varHostSshIp = input("安装kgx主机（例如： 192.168.1.20:22）：")
                varHostSshUser = input("安装kgx主机的SSH用户（默认 root）：") or "root"
                varHostSshPassword = getpass.getpass("输入SSH密码：")

            varSudoPassword = getpass.getpass("输入sudo密码，如果当前为root用户不需要输入：")

            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_kgx_install.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                    varHostSshPassword, varSudoPassword,
                                                    varInstallLocally.lower() == "y")

            cli_common.execute_command(var_command)
