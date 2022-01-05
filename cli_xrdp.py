# coding:utf-8

import cli_common
import os


class XrdpCli(object):
    """
    Cli for managing xrdp. OS support: centOS8、ubuntu
    """

    def install(self):
        """
        Install xrdp.

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_install = raw_input("安装xrdp吗? [y/n]: ")
        if var_install.lower() == "y":
            var_host_target = raw_input("请输入目标主机ip地址（例如： 192.168.1.20:8080）： ")
            var_host_target_user = raw_input("请输入目标主机登录用户（默认： root）： ") or "root"

        if var_install.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_xrdp_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user)
            cli_common.execute_command(var_command)