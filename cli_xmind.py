# coding:utf-8

import cli_common
import os


class XmindCli(object):
    """
    Cli for managing xmind. OS support: ubuntu
    """

    def install(self):
        """
        Install xmind.

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_install = input("安装xmind吗? [y/n]: ")
        if var_install.lower() == "y":
            var_host_target = input("请输入目标主机ip地址（例如： 192.168.1.20:8080）： ")
            var_host_target_user = input("请输入目标主机登录用户（默认： root）： ") or "root"

        if var_install.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_xmind_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user)
            cli_common.execute_command(var_command)