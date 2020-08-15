import cli_common


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

        if from_source:
            var_command = "ansible-playbook role_openresty_install.yml"
            cli_common.execute_command(var_command)
        else:
            # TODO: Install openresty from yum repository
            raise Exception, "Install openresty from yum repository not implement yet."