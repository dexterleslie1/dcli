import cli_common
import os


class OpenrestyCli(object):
    """
    Cli for managing openresty.
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
            var_command = "ansible-playbook " + var_full_path + "/role_openresty_install.yml"
            cli_common.execute_command(var_command)
        else:
            # TODO: Install openresty from yum repository
            raise Exception, "Install openresty from yum repository not implement yet."