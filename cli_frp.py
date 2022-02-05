# coding:utf-8

import cli_common
import os


class FrpCli(object):
    """
    Cli for managing frp. OS support: centOS8
    """

    def install(self):
        """
        Install frp.

        :return:
        """

        # 询问用户是否安装frp服务器或者客户端
        var_install_frp_server = input("是否安装frp服务器? [y/n]: ")
        var_install_frp_client = "n"
        if var_install_frp_server.lower() != "y":
            var_install_frp_client = input("是否安装frp客户端? [y/n]: ")

        if var_install_frp_server.lower() == "y" or var_install_frp_client.lower() == "y":
            # Full path of python file locates in
            var_full_path = os.path.dirname(os.path.realpath(__file__))

            var_host_target = input("Enter deploying target machine (example: 192.168.1.20:8080): ")
            var_host_target_user = input("Enter target machine user (default root): ") or "root"

            # 安装frp服务器需要提供监听端口、身份鉴别token
            # 安装frp客户端需要提供frp服务器地址、端口、身份鉴别token
            var_frp_server_ip = ""
            var_frp_server_port = "0"
            var_frp_privilege_token = ""
            if var_install_frp_client.lower() == "y":
                var_frp_server_ip = input("输入frp服务器ip地址（NOTE：不提供则使用默认配置的）: ") or ""
            var_frp_server_port = input("输入frp服务器端口（NOTE：不提供则使用默认配置的）: ") or "0"
            var_frp_privilege_token = input("输入frp服务器身份鉴别token（NOTE：不提供则使用默认配置的）: ") or ""

            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_frp_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user)

            if var_install_frp_server.lower() == "y":
                var_command = var_command + " -e varInstallFrpServer=true"
            if var_install_frp_client.lower() == "y":
                var_command = var_command + " -e varInstallFrpClient=true"

            var_command = var_command + " -e varFrpServerIp=" + var_frp_server_ip
            var_command = var_command + " -e varFrpServerPort=" + var_frp_server_port
            var_command = var_command + " -e varFrpToken=" + var_frp_privilege_token

            cli_common.execute_command(var_command)