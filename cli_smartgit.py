import cli_common
import os
import getpass


class SmartgitCli(object):
    """
    Cli for managing smartgit. OS support: centOS8
    """

    def install(self):
        """
        Install smartgit.

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_install = input("Install smartgit? [y/n]: ")
        if var_install.lower() == "y":
            varInstallLocally = input("是否本地安装？ [y/n]: ") or "n"
            var_host_target = ""
            var_host_target_user = ""
            varSshPassword = ""

            if not varInstallLocally.lower() == "y":
                var_host_target = input("输入目标主机IP（例如： 192.168.1.20:8080）：")
                var_host_target_user = input("输入目标主机SSH用户（默认 root）：") or "root"
                varSshPassword = getpass.getpass("输入SSH密码：")

            varSudoPassword = getpass.getpass("输入主机的sudo密码，如果当前为root用户不需要输入：")

            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_smartgit_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user, varSshPassword,
                                                    varSudoPassword, varInstallLocally.lower() == "y")
            cli_common.execute_command(var_command)
