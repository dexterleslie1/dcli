import cli_common
import os
import logging


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

        var_install = input("Install Shadowsocks? [y/n]: ")
        if var_install.lower() == "y":
            var_host_target = input("Enter target deploying machine (example: 192.168.1.20:8080): ")
            var_host_target_user = input("Enter target machine user (default root): ") or "root"
            var_server_port = input("Enter server port (default 11080): ") or "11080"
            var_password = input("Enter password (default 123456): ") or "123456"
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_shadowsocks_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user)
            if var_server_port:
                var_command = var_command + " -e var_server_port=" + var_server_port
            if var_password:
                var_command = var_command + " -e var_password=" + var_password
            cli_common.execute_command(var_command)
