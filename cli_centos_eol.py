# coding:utf-8

import cli_common
import os


class CentOSEolCli(object):
    """
    centOS8 eol管理工具. OS support: centOS8
    """

    def config(self):
        """
        配置centOS8 eol

        :return:
        """

        # 询问用户是否配置centOS8 eol
        var_agree = input("是否配置centOS EOL？ [y/n]：")
        if var_agree.lower() == "y" :

            var_install_locally = input("是否本地安装？ [y/n]: ") or "n"
            if not var_install_locally == "y":
                var_host_target = input("目标主机（例如： 192.168.1.20:8080）：")
                var_host_target_user = input("目标主机SSH用户（默认 root）：") or "root"

            # Full path of python file locates in
            var_full_path = os.path.dirname(os.path.realpath(__file__))

            if var_install_locally == "y":
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_centos_eol_config.yml --connection=local -i 127.0.0.1,"
            else:
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_centos_eol_config.yml"
                var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user)

            cli_common.execute_command(var_command)