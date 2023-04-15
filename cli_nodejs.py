# coding:utf-8

import cli_common
import os
import getpass
import enquiries


class NodejsCli(object):
    """
    Cli for managing nodejs. OS support: Ubuntu
    """

    def install(self):
        """
        Install nodejs.

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        varSshIp = ""
        varSshUser = ""
        varSshPassword = ""
        varInstallLocally = "n"
        varSudoPassword = ""

        varInstall = input("是否安装nodejs？ [y/n]: ")
        if varInstall.lower() == "y":

            # 选择nodejs安装版本
            varOptions = ["v15.14.0", "v16.20.0"]
            varVersion = enquiries.choose("选择版本：", varOptions)

            varInstallLocally = input("是否本地安装？ [y/n]: ") or "n"

            if not varInstallLocally.lower() == "y":
                varSshIp = input("输入目标主机IP（例如： 192.168.1.20:8080）：")
                varSshUser = input("输入目标主机SSH用户（默认 root）：") or "root"
                varSshPassword = getpass.getpass("输入SSH密码：")

            varSudoPassword = getpass.getpass("输入当前主机的sudo密码，如果当前为root用户不需要输入：")

            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_nodejs_install.yml"
            var_command = cli_common.concat_command(var_command, varSshIp, varSshUser, varSshPassword, varSudoPassword,
                                                    varInstallLocally.lower() == "y")

            if varVersion:
                var_command = var_command + " -e varVersion=" + varVersion

            cli_common.execute_command(var_command)

            print("使用命令设置yarn全局仓库指向淘宝，yarn config set registry https://registry.npm.taobao.org/ -g")
            print("使用命令获取当前yarn全局仓库，yarn config get registry -g")
            print("使用命令设置yarn仓库指向淘宝，yarn config set registry https://registry.npm.taobao.org/")
            print("使用命令获取当前yarn仓库，yarn config get registry")
            print("成功安装nodejs" + varVersion + "，重新启动操作系统以便正确加载nodejs环境变量")
