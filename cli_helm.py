import cli_common
import os
import getpass


class Helm(object):
    """
    helm管理工具。支持操作系统： centOS8
    """

    def install(self):
        """
        安装helm

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        varSshIp = ""
        varSshUser = ""
        varSshPassword = ""
        varInstallLocally = "n"
        varSudoPassword = ""

        varInstall = input("是否安装helm？ [y/n]: ")
        if varInstall.lower() == "y":
            varInstallLocally = input("是否本地安装？ [y/n]: ") or "n"

            if not varInstallLocally.lower() == "y":
                varSshIp = input("输入目标主机IP（例如： 192.168.1.20:8080）：")
                varSshUser = input("输入目标主机SSH用户（默认 root）：") or "root"
                varSshPassword = getpass.getpass("输入SSH密码：")

            varSudoPassword = getpass.getpass("输入当前主机的sudo密码，如果当前为root用户不需要输入：")

        if varInstall.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_helm_config.yml"
            var_command = cli_common.concat_command(var_command, varSshIp, varSshUser, varSshPassword, varSudoPassword, varInstallLocally.lower() == "y")
            cli_common.execute_command(var_command)

            print("helm cli安装成功，如果安装目标主机不为kubernetes主机，则需要手动配置~/.kube/config配置")
