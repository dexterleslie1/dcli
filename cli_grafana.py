import cli_common
import os


class GrafanaCli(object):
    """
    Cli for managing grafana. OS support: centOS8
    """

    def install(self):
        """
        Install grafana.

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_install = input("Install grafana? [y/n]: ")
        if var_install.lower() == "y":
            var_host_prometheus = input("Enter target machine of deploying grafana (example: 192.168.1.20:8080): ")
            var_host_prometheus_user = input("Enter target machine user (default root): ") or "root"
            # var_grafana_admin = input("Enter grafana admin user or left it empty without changing: ")
            # var_grafana_admin_password = input("Enter grafana admin user password or left it empty without changing: ")

        # Install grafana
        if var_install.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_grafana_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_prometheus, var_host_prometheus_user)
            # if var_grafana_admin:
            #     var_command = var_command + " -e var_grafana_admin=" + var_grafana_admin
            # if var_grafana_admin_password:
            #     var_command = var_command + " -e var_grafana_admin_password=" + var_grafana_admin_password
            cli_common.execute_command(var_command)
