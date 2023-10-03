import enquiries

import cli_common


class K8sCli(object):
    """
    k8s管理工具。支持操作系统： centOS8
    """

    def install(self, install=None, target_host=None, target_host_user='root', target_host_password=None,
                sudo_password=None,
                mode=None, hostname="", hostip=""):
        """
        安装和配置k8s

        :param install: 是否安装和配置Jmeter？ [y/n]
        :param target_host: 目标主机（例如： 192.168.1.20:8080）
        :param target_host_user: 目标主机SSH用户（默认 root）
        :param target_host_password: 目标主机SSH密码
        :param sudo_password: 目标主机的sudo密码，如果当前为root用户不需要输入
        :param mode: k8s安装模式，master或者worker
        :param hostname: 主机hostname
        :param hostip: 主机ip地址
        :return:
        """

        unattended_intall, var_command, install = \
            cli_common.prompt("k8s", install, target_host, target_host_user, target_host_password, sudo_password,
                              ansible_role_file="role_k8s_install.yml")

        if install.lower() == "y":
            if not unattended_intall:
                options = ["master", "worker"]
                mode = enquiries.choose("选择k8s安装和配置模式：", options)

            if mode == "master":
                if not unattended_intall:
                    hostname = input("输入hostname（默认k8s-master）： ") or "k8s-master"
                    hostip = input("输入host ip： ")

                if len(hostname.strip()) == 0:
                    hostname = "k8s-master"

                if len(hostip.strip()) == 0:
                    raise Exception("必须输入host ip！")

                var_command = var_command + " -e varSetHostname=true -e varHostname=\"" + hostname + "\""
                var_command = var_command + " -e varHostIp=\"" + hostip + "\""
                var_command = var_command + " -e varMasterNode=true"

            else:
                if not unattended_intall:
                    hostname = input("输入hostname： ")

                if len(hostname.strip()) == 0:
                    raise Exception("必须输入hostname！")

                var_command = var_command + " -e varSetHostname=true -e varHostname=\"" + hostname + "\""

            cli_common.execute_command(var_command)

            print("提示： -------------------------------------------------------------"
                  "\n在master节点运行kubeadm token create --print-join-command获取加入worker节点命令"
                  "\n在worker节点运行kubeadm join命令加入master节点"
                  "\n在master节点运行kubectl get pods -n kube-system查看master节点基础容器运行状态"
                  "\n在master节点运行kubectl get nodes查看所有节点状态")
