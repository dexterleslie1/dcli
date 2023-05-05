# coding:utf-8

import cli_common
import os
import getpass


class DockerCli(object):
    """
    Cli for managing docker. OS support: centOS7、centOS8、ubuntu
    """

    def install(self):
        """
        安装docker，ubuntu系统时，在安装完docker后，需要使用命令手动添加指定用户到docker组，例如：sudo usermod -a -G docker testuser1，
        否则用户执行docker相关命令都需要添加sudo，注意：把用户添加到docker组后需要logout用户再login才能生效

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_host_target = ""
        var_host_target_user = ""
        varSshPassword = ""
        varSudoPassword = ""

        var_install = input("是否安装docker？ [y/n]: ")
        if var_install.lower() == "y":
            var_install_locally = input("是否本地安装？ [y/n]: ") or "n"
            if not var_install_locally == "y":
                var_host_target = input("安装主机（例如： 192.168.1.20:8080）： ")
                var_host_target_user = input("安装主机的SSH用户（默认 root）： ") or "root"
                varSshPassword = getpass.getpass("输入SSH密码：")

            varSudoPassword = getpass.getpass("输入主机的sudo密码，如果当前为root用户不需要输入：")

            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_docker_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user,
                                                    varSshPassword, varSudoPassword,
                                                    var_install_locally.lower() == "y")
            cli_common.execute_command(var_command)

            print("安装完成后重启系统以加载最新环境变量，否则docker-compose使用时报告异常")
