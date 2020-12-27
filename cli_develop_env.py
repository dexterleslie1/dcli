import cli_common
import os


class DevelopEnvCli(object):
    """
    Cli for managing develop environment. Java etc. Support OS: centOS8
    """

    def install(self,
                remote_hosts="127.0.0.1,",
                remote_user="root",
                include_jdk=False,
                include_git=False,
                include_maven=False,
                include_mariadb=False,
                include_redis=False,
                include_intellij=False,
                include_smartgit=False):
        """
        Install develop environment.

        :param remote_hosts
        :param remote_user
        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))
        var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_develop_env_install.yml"
        var_command = cli_common.concat_command(var_command, remote_hosts, remote_user)

        if include_jdk:
            var_command = var_command + " -e var_include_jdk=true"
        if include_git:
            var_command = var_command + " -e var_include_git=true"
        if include_maven:
            var_command = var_command + " -e var_include_maven=true"
        if include_mariadb:
            var_command = var_command + " -e var_include_mariadb=true"
        if include_redis:
            var_command = var_command + " -e var_include_redis=true"
        if include_intellij:
            var_command = var_command + " -e var_include_intellij=true"
        if include_smartgit:
            var_command = var_command + " -e var_include_smartgit=true"

        cli_common.execute_command(var_command)
