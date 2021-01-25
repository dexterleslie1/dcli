import cli_common
import os


class PrometheusCli(object):
    """
    Cli for managing prometheus. OS support: centOS8
    """

    def install(self):
        """
        Install prometheus.

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_prometheus_install.yml"
        var_command = var_command + " --user root"
        var_command = var_command + " --ask-pass"
        cli_common.execute_command(var_command)