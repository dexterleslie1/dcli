import cli_common
import os


class FreeswitchCli(object):
    """
    Cli for managing freeswitch.
    """

    def setup(self, socks5=None):
        """
        Call ansible role_freeswitch_install role to install freeswitch.

        :param socks5:
            Socks5 proxy server to accelerate yum install freeswitch.
            Value should be in format 192.168.1.12:10080
        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        # Call ansible-playbook command with role_freeswitch_install.yml file
        var_command = "ansible-playbook " + var_full_path + "/role_freeswitch_install.yml"

        if socks5:
            var_command = var_command + " -e socks5=socks5h://" + socks5

        cli_common.execute_command(var_command)
