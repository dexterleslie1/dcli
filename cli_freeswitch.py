import cli_common
import os


class FreeswitchCli(object):
    """
    Cli for managing freeswitch
    """

    def setup(self):
        """
        Call ansible role_freeswitch_install role to install freeswitch
        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        # Call ansible-playbook command with role_freeswitch_install.yml file
        var_command = "ansible-playbook " + var_full_path + "/role_freeswitch_install.yml"
        cli_common.execute_command(var_command)
