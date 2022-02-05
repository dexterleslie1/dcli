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

        var_install_prometheus = input("Install prometheus? [y/n]: ")
        if var_install_prometheus.lower() == "y":
            var_host_prometheus = input("Enter target machine of deploying prometheus (example: 192.168.1.20:8080): ")
            var_host_prometheus_user = input("Enter target machine user (default root): ") or "root"
            var_host_pushgateway_1 = input("* Enter pushgateway (example: 192.168.1.20): ")
            if not var_host_pushgateway_1:
                raise Exception("Parameter pushgateway cann't be empty")

        var_install_pushgateway = input("Install pushgateway? [y/n]: ")
        if var_install_pushgateway.lower() == "y":
            var_host_pushgateway = input("Enter target machine of deploying pushgateway (example: 192.168.1.20:8080): ")
            var_host_pushgateway_user = input("Enter target machine user (default root): ") or "root"

        # Install prometheus
        if var_install_prometheus.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_prometheus_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_prometheus, var_host_prometheus_user)
            var_command = var_command + " -e var_host_pushgateway=" + var_host_pushgateway_1
            cli_common.execute_command(var_command)

        # Install pushgateway
        if var_install_pushgateway.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_prometheus_pushgateway_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_pushgateway, var_host_pushgateway_user)
            cli_common.execute_command(var_command)
