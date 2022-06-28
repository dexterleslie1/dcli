# coding:utf-8

import cli_common
import os
import getpass


class MavenCli(object):
    """
    Cli for managing maven. OS support: centOS8、Ubuntu
    """

    def install(self):
        """
        Install maven.

        :return:
        """

        var_install = input("是否安装maven? [y/n]: ")

        if var_install.lower() == "y":
            # Full path of python file locates in
            var_full_path = os.path.dirname(os.path.realpath(__file__))

            varInstallLocally = input("是否本地安装？ [y/n]: ") or "n"
            var_host_target = ""
            var_host_target_user = ""
            varSshPassword = ""

            if not varInstallLocally.lower() == "y":
                var_host_target = input("输入目标主机IP（例如： 192.168.1.20:8080）：")
                var_host_target_user = input("E输入目标主机SSH用户（默认 root）：") or "root"
                varSshPassword = getpass.getpass("输入SSH密码：")

            varSudoPassword = getpass.getpass("输入主机的sudo密码，如果当前为root用户不需要输入：")

            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_maven_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user, varSshPassword,
                                                    varSudoPassword, varInstallLocally.lower() == "y")

            cli_common.execute_command(var_command)