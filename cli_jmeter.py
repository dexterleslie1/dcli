import cli_common
import os
import enquiries
import getpass


class JmeterCli(object):
    """
    Jmeter管理工具。支持操作系统： centOS8
    """

    def install(self, install=None, target_host=None, target_host_user='root', target_host_password=None,
                sudo_password=None,
                mode=None, remote_hosts=None, slave_listen_ip=None, xmx=1):
        """
        安装和配置Jmeter

        :param install: 是否安装和配置Jmeter？ [y/n]
        :param target_host: 目标主机（例如： 192.168.1.20:8080）
        :param target_host_user: 目标主机SSH用户（默认 root）
        :param target_host_password: 目标主机SSH密码
        :param sudo_password: 目标主机的sudo密码，如果当前为root用户不需要输入
        :param mode: jmeter安装模式，master或者slave
        :param remote_hosts: jmeter.properties remote_hosts设置（例如：192.168.1.1,192.168.1.2，多个主机之间用逗号分开）
        :param slave_listen_ip: slave模式rmi监听的ip地址
        :param xmx: jmeter最大java堆内存，单位GB（默认1GB）
        :return:
        """

        # 无人值守安装
        unattended_intall = install and install.strip() == "y"

        if not unattended_intall:
            install = input("是否安装和配置Jmeter？ [y/n]：") or "n"

        if install.lower() == "y":

            if not unattended_intall:
                install_locally = input("是否本地安装？ [y/n]: ") or "n"
            else:
                install_locally = "y" if not target_host or not target_host.strip() else "n"

            if not unattended_intall and not install_locally == "y":
                target_host = input("目标主机（例如： 192.168.1.20:8080）：")
                target_host_user = input("目标主机SSH用户（默认 root）：") or "root"
                target_host_password = getpass.getpass("输入SSH密码：")

            if not unattended_intall:
                sudo_password = getpass.getpass("输入主机的sudo密码，如果当前为root用户不需要输入：")

            # Full path of python file locates in
            var_full_path = os.path.dirname(os.path.realpath(__file__))

            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_jmeter_install.yml"
            var_command = cli_common.concat_command(var_command, target_host, target_host_user
                                                    , target_host_password, sudo_password,
                                                    install_locally.lower() == "y", unattended_intall)

            if not unattended_intall:
                options = ["master", "slave"]
                mode = enquiries.choose("选择Jmeter安装和配置模式：", options)

            if mode == "master":

                if not unattended_intall:
                    remote_hosts = input("输入jmeter.properties remote_hosts设置（例如：192.168.1.1,192.168.1.2，多个主机之间用逗号分开）：")

                var_command = var_command + " -e varRemoteHosts=" + remote_hosts
                var_command = var_command + " -e varMasterMode=true"
            else:

                if not unattended_intall:
                    slave_listen_ip = input("* 输入Jmeter slave模式rmi监听的ip地址：")

                if not slave_listen_ip or not slave_listen_ip.strip():
                    raise Exception("必须输入Jmeter slave模式rmi监听的ip地址！")

                var_command = var_command + " -e varRmiListenIp=" + slave_listen_ip
                var_command = var_command + " -e var_slave_mode=true"

            if not unattended_intall:
                # 当安装Jmeter时，提示输入Jmeter -Xmx内存值
                xmx = input("输入Jmeter最大java堆内存，单位GB（默认1GB）：") or 1
                xmx = int(xmx)

            var_command = var_command + " -e var_heap_mx=" + str(xmx)

            cli_common.execute_command(var_command)
