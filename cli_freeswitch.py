import cli_common
import os


class FreeswitchCli(object):
    """
    Cli for managing freeswitch. OS support: centOS7
    """

    def install(self, socks5=None, remote_hosts="127.0.0.1,", remote_user="root"):
        """
        Call ansible role_freeswitch_install role to install freeswitch.

        :param socks5:
            Socks5 proxy server to accelerate yum install freeswitch.
            Value should be in format 192.168.1.12:10080
        :param remote_hosts
        :param remote_user
        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        # Call ansible-playbook command with role_freeswitch_install.yml file
        var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_freeswitch_install.yml"

        if socks5:
            var_command = var_command + " -e socks5=socks5h://" + socks5
        var_command = cli_common.concat_command(var_command, remote_hosts, remote_user)
        cli_common.execute_command(var_command)
