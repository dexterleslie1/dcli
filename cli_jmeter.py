import cli_common
import enquiries


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

        unattended_intall, var_command, install = \
            cli_common.prompt("jmeter", install, target_host, target_host_user, target_host_password, sudo_password,
                              ansible_role_file="role_jmeter_install.yml")

        if install.lower() == "y":
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
