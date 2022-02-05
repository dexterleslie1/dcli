import cli_common
import os
import logging


class OpenrestyCli(object):
    """
    Cli for managing openresty. OS support: centOS8
    """

    def install(self, from_source=True):
        """
        Install openresty.

        :param from_source:
            When true install openresty from source code.
            When false install openresty from yum repository.
        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        if from_source:
            var_compile = input("Compile Openresty? [y/n]: ")
            var_install = input("Install Openresty? [y/n]: ")
            if var_compile.lower() == "y":
                # Compile openresty on compile machine
                logging.info("########################### Compile openresty ##############################")
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_openresty_compile.yml"
                var_command = var_command + " --user root"
                var_command = var_command + " --ask-pass"
                cli_common.execute_command(var_command)

            if var_install.lower() == "y":
                # Deploy openresty to target machine
                logging.info("########################### Deploy openresty ##############################")
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_openresty_install.yml"
                var_command = var_command + " --user root"
                var_command = var_command + " --ask-pass"
                cli_common.execute_command(var_command)
        else:
            # TODO: Install openresty from yum repository
            raise Exception("Install openresty from yum repository not implement yet.")