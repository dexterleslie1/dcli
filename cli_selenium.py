import cli_common
import os
import enquiries
import getpass


class SeleniumCli(object):
    """
    selenium管理工具。支持操作系统： Ubuntu
    """

    def install(self):
        """
        安装和配置selenium

        :return:
        """

        # Full path of python file locates in
        varFullPath = os.path.dirname(os.path.realpath(__file__))

        varInstall = input("是否安装和配置selenium？ [y/n]： ") or "n"
        varInstallLocally = "n"
        varHostSshIp = ""
        varHostSshUser = ""
        varHostSshPassword = ""
        varSudoPassword = ""

        if varInstall.lower() == "y":
            varInstallLocally = input("是否本地安装配置？ [y/n]: ") or "n"
            if not varInstallLocally == "y":
                varHostSshIp = input("主机（例如： 192.168.1.20:8080）：")
                varHostSshUser = input("主机的SSH用户（默认 root）：") or "root"
                varHostSshPassword = getpass.getpass("输入SSH密码：")

            varSudoPassword = getpass.getpass("输入主机的sudo密码，如果当前为root用户不需要输入：")

            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_selenium_install.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser, varHostSshPassword, varSudoPassword, varInstallLocally.lower() == "y")
            cli_common.execute_command(var_command)
