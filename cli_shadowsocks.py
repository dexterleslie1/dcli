import cli_common
import os
import logging
import getpass
import enquiries


class ShadowsocksCli(object):
    """
    Cli for managing shadowsocks. OS support: centOS8
    """

    def install(self):
        """
        Install shadowsocks.
        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_install = input("是否安装Shadowsocks? [y/n]: ")
        if var_install.lower() == "y":
            var_host_target = ""
            var_host_target_user = ""
            varDeploymentHostSshPassword = ""

            var_options = ["服务器", "客户端"]
            var_choose = enquiries.choose("选择安装类型：", var_options)

            var_install_locally = input("是否本地部署？ [y/n]: ") or "n"
            if not var_install_locally == "y":
                var_host_target = input("部署主机（例如： 192.168.1.20:8080）：")
                var_host_target_user = input("部署主机的SSH用户（默认 root）：") or "root"
                varDeploymentHostSshPassword = getpass.getpass("输入SSH密码：")

            varSudoPasswordDeployment = getpass.getpass("输入部署主机的sudo密码，如果当前为root用户不需要输入：")

            var_server_port = None
            var_password = None
            var_install_server = var_choose == "服务器"

            if var_choose == "服务器":
                var_server_port = input("ss服务器端口（默认 11080）： ") or "11080"
                var_password = input("ss服务器密码（默认 123456）： ") or "123456"

            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_shadowsocks_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user,
                                                    varDeploymentHostSshPassword
                                                    , varSudoPasswordDeployment, var_install_locally.lower() == "y")
            if var_server_port:
                var_command = var_command + " -e var_server_port=" + var_server_port
            if var_password:
                var_command = var_command + " -e var_password=" + var_password

            var_command = var_command + " -e var_install_server=" + str(var_install_server)

            cli_common.execute_command(var_command)

            if var_choose == "客户端":
                print("shadowsocks客户端已经成功安装，需要手动配置/etc/shadowsocks-client.json后systemctl restart shadowsocks-client，"
                      "使用命令测试shadowsocks客户端是否配置成功curl --socks5-hostname shadowsocks客户端ip:1080 http://www.google.com")
