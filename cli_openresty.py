import cli_common
import os


class OpenrestyCli(object):
    """
    Cli for managing openresty.
    """

    def install(self, from_source=True, remote_hosts="127.0.0.1,", remote_user="root"):
        """
        Install openresty.

        :param from_source:
            When true install openresty from source code.
            When false install openresty from yum repository.
        :param remote_hosts
        :param remote_user
        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        if from_source:
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_openresty_install.yml"
            var_command = cli_common.concat_command(var_command, remote_hosts, remote_user)
            cli_common.execute_command(var_command)
        else:
            # TODO: Install openresty from yum repository
            raise Exception, "Install openresty from yum repository not implement yet."