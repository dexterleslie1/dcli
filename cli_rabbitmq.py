import cli_common
import os


class RabbitmqCli(object):
    """
    Cli for managing rabbitmq. OS support: centOS8
    """

    def install(self):
        """
        Call ansible role_rabbitmq_install role to install rabbitmq.
        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_install = raw_input("Install RabbitMQ? [y/n]: ")
        if var_install.lower() == "y":
            var_host_target_rabbitmq = raw_input("Enter deploying target machine (example: 192.168.1.20:8080): ")
            var_host_target_user_rabbitmq = raw_input("Enter target machine user (default root): ") or "root"

        if var_install.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_rabbitmq_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target_rabbitmq, var_host_target_user_rabbitmq)
            cli_common.execute_command(var_command)
