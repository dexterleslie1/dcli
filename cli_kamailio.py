import cli_common
import os


class KamailioCli(object):
    """
    Cli for managing kamailio. OS support: centOS8
    """

    def install(self, socks5=None, remote_hosts="127.0.0.1,", remote_user="root"):
        """
        Call ansible role_kamailio_install role to install kamailio.

        :param remote_hosts
        :param remote_user
        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        # Call ansible-playbook command with role_kamailio_install.yml file
        var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_kamailio_install.yml"
        var_command = cli_common.concat_command(var_command, remote_hosts, remote_user)
        cli_common.execute_command(var_command)
