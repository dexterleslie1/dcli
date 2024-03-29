import cli_common
import os


class MongodbCli(object):
    """
    Cli for managing mongodb. OS support: centOS8
    """

    def install(self):
        """
        Install mongodb

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_install = input("Install Mongodb? [y/n]: ")
        if var_install.lower() == "y":
            var_host_target = input("Enter deploying target machine (example: 192.168.1.20:8080): ")
            var_host_target_user = input("Enter target machine user (default root): ") or "root"

        if var_install.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_mongodb_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user)
            cli_common.execute_command(var_command)
