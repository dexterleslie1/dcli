# coding:utf-8

import cli_common
import os


class JdkCli(object):
    """
    管理jdk。 支持的系统: centOS、debian10、ubuntu
    """

    def install(self):
        """
        安装jdk

        :return:
        """

        varInstallJdk = input("是否安装jdk？ [y/n]: ")

        if varInstallJdk.lower() == "y":
            var_full_path = os.path.dirname(os.path.realpath(__file__))

            var_host_target = input("请输入目标主机ip地址（例如： 192.168.1.20:8080）： ")
            var_host_target_user = input("请输入目标主机登录用户（默认： root）： ") or "root"

            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_jdk_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user)

            cli_common.execute_command(var_command)