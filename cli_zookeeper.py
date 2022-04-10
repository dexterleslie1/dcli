import cli_common
import os
import getpass


class ZookeeperCli(object):
    """
    Zookeeper管理工具。支持操作系统： centOS8
    """

    def install(self):
        """
        安装Zookeeper

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        varHostIp = ""
        varHostUser = ""
        varHostPassword = ""
        varInstallLocally = "n"
        varPort = 2181

        varInstall = input("是否安装Zookeeper？ [y/n]: ")
        if varInstall.lower() == "y":
            varPort = input("输入Zookeeper监听端口（默认2181）: ") or 2181

            varInstallLocally = input("是否本地安装？ [y/n]: ") or "n"

            if not varInstallLocally.lower() == "y":
                varHostIp = input("输入目标主机IP（例如： 192.168.1.20:8080）：")
                varHostUser = input("输入目标主机SSH用户（默认 root）：") or "root"
                varHostPassword = getpass.getpass("输入SSH密码：")

        if varInstall.lower() == "y":
            if varInstallLocally.lower() == "y":
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_zookeeper_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
            else:
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_zookeeper_install.yml"
                var_command = cli_common.concat_command(var_command, varHostIp, varHostUser, varHostPassword)

            var_command = var_command + " -e varPort=" + str(varPort)

            cli_common.execute_command(var_command)