import cli_common
import os
import logging


class OpenrestyCli(object):
    """
    openresty管理工具。支持操作系统： centOS8
    """

    def install(self, from_source=True):
        """
        安装openresty

        :param from_source:
            true 从源代码安装openresty，需要指定编译openresty主机。
            false 从yum安装openresty。
        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_compile_locally = "n"
        var_install_locally = "n"
        if from_source:
            var_compile = input("是否编译openresty？ [y/n]： ")
            var_install = input("安装openresty？ [y/n]： ")
            if var_compile.lower() == "y":
                var_compile_locally = input("是否本地编译openresty？ [y/n]: ") or "n"
                if not var_compile_locally == "y":
                    var_host_target = input("编译openresty主机（例如： 192.168.1.20:8080）：")
                    var_host_target_user = input("编译openresty主机的SSH用户（默认 root）：") or "root"

            if var_install.lower() == "y":
                var_install_locally = input("是否本地部署openresty？ [y/n]: ") or "n"
                if not var_install_locally == "y":
                    var_host_target = input("部署openresty主机（例如： 192.168.1.20:8080）：")
                    var_host_target_user = input("部署openresty主机的SSH用户（默认 root）：") or "root"

            if var_compile.lower() == "y":
                # 在编译主机中编译openresty
                logging.info("########################### 编译openresty ##############################")

                if var_compile_locally == "y":
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_openresty_compile.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                else:
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_openresty_compile.yml"
                    var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user)
                cli_common.execute_command(var_command)

            if var_install.lower() == "y":
                # 部署openresty
                logging.info("########################### 部署openresty ##############################")

                if var_install_locally == "y":
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_openresty_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                else:
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_openresty_install.yml"
                    var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user)
                cli_common.execute_command(var_command)
        else:
            # TODO: Install openresty from yum repository
            raise Exception("Install openresty from yum repository not implement yet.")