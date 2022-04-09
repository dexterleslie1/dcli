import cli_common
import os
import getpass
import enquiries


class RedisCli(object):
    """
    Redis管理工具。支持操作系统： centOS8
    """

    def install(self):
        """
        安装Redis

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        varHostRedisIp = ""
        varHostRedisUser = ""
        varHostRedisPassword = ""
        varRedisPassword = ""
        varRedisPort = ""
        varRedisMode = "";
        varInstallLocally = "n"
        varReboot  = "n"

        varInstall = input("是否安装Redis？ [y/n]: ")
        if varInstall.lower() == "y":
            # 询问是否重启操作系统
            varReboot = input("完成安装redis后是否重启操作系统使内核调整参数生效？ [y/n]: ") or "n"

            # 询问安装单机版redis还是安装集群版redis
            varOptions = ["单机版", "集群版"]
            varRedisMode = enquiries.choose(
                "选择安装单机版还是集群版redis：", varOptions)
            if varRedisMode == "单机版":
                varRedisPort = input("设置redis端口（默认：6379）：") or "6379"
                varRedisPassword = getpass.getpass("设置redis密码：")
            else:
                raise Exception("未实现")

            varInstallLocally = input("是否本地安装？ [y/n]: ") or "n"

            if not varInstallLocally.lower() == "y":
                varHostRedisIp = input("输入目标主机IP（例如： 192.168.1.20:8080）：")
                varHostRedisUser = input("输入目标主机SSH用户（默认 root）：") or "root"
                varHostRedisPassword = getpass.getpass("输入SSH密码：")

        if varInstall.lower() == "y":
            if varInstallLocally.lower() == "y":
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_redis_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
            else:
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_redis_install.yml"
                var_command = cli_common.concat_command(var_command, varHostRedisIp, varHostRedisUser, varHostRedisPassword)

            if varRedisMode == "单机版":
                var_command = var_command + " -e varRedisMode=standalone"
            else:
                var_command = var_command + " -e varRedisMode=cluster"

            if len(varRedisPort) > 0:
                var_command = var_command + " -e varRedisPort=" + varRedisPort

            if varReboot.lower() == "y":
                var_command = var_command + " -e varReboot=true"
            else:
                var_command = var_command + " -e varReboot=false"

            if len(varRedisPassword) > 0:
                var_command = var_command + " -e varRedisPassword=\"" + varRedisPassword + "\""

            cli_common.execute_command(var_command)