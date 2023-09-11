# coding:utf-8

import cli_common
import enquiries


class LocustCli(object):
    """
    Cli for managing locust. OS support: centOS8
    """

    def install(self, install=None, target_host=None, target_host_user='root', target_host_password=None,
                sudo_password=None,
                mode=None, master_host=None, slave_cpu_count=None):
        """
        安装locust master和slave

        :param install: 是否安装和配置Jmeter？ [y/n]
        :param target_host: 目标主机（例如： 192.168.1.20:8080）
        :param target_host_user: 目标主机SSH用户（默认 root）
        :param target_host_password: 目标主机SSH密码
        :param sudo_password: 目标主机的sudo密码，如果当前为root用户不需要输入
        :param mode: locust安装模式，master或者slave
        :param master_host: locust master ip
        :param slave_cpu_count: locust slave cpu个数，会根据cpu个数启动对应个数的slave进程
        :return:
        """

        unattended_intall, var_command, install = \
            cli_common.prompt("locust", install, target_host, target_host_user, target_host_password, sudo_password,
                              ansible_role_file="role_locust_install.yml")

        if install.lower() == "y":

            if not unattended_intall:
                options = ["master", "slave"]
                mode = enquiries.choose("选择locust安装和配置模式：", options)

            if mode == "master":
                var_command = var_command + " -e mode_master=True"
            else:

                if not unattended_intall:
                    master_host = input("locust master ip地址：")

                if not unattended_intall:
                    slave_cpu_count = input("locust slave cpu个数：") or 0

                if not master_host or not master_host.strip():
                    raise Exception("必须输入locust master ip地址！")
                if not slave_cpu_count or int(slave_cpu_count) <= 0:
                    raise Exception("必须指定locust slave cpu个数！")

                var_command = var_command + " -e mode_slave=True"
                var_command = var_command + " -e cpu_count=" + str(slave_cpu_count)
                var_command = var_command + " -e master_host=" + master_host

            cli_common.execute_command(var_command)
