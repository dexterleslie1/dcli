import cli_common
import os
import enquiries
import getpass


class K8sCli(object):
    """
    k8s管理工具。支持操作系统： centOS7
    """

    def install(self):
        """
        安装和配置k8s

        :return:
        """

        # Full path of python file locates in
        varFullPath = os.path.dirname(os.path.realpath(__file__))

        varInstall = input("是否安装和配置k8s？ [y/n]： ") or "n"
        varInstallLocally = "n"
        varHostSshIp = ""
        varHostSshUser = ""
        varHostSshPassword = ""
        varSudoPassword = ""

        if varInstall.lower() == "y":
            varInstallLocally = input("是否本地安装配置？ [y/n]: ") or "n"
            if not varInstallLocally == "y":
                varHostSshIp = input("主机（例如： 192.168.1.20:8080）：")
                varHostSshUser = input("主机的SSH用户（默认 root）：") or "root"
                varHostSshPassword = getpass.getpass("输入SSH密码：")

            varSudoPassword = getpass.getpass("输入主机的sudo密码，如果当前为root用户不需要输入：")

            varOptions = ["安装和配置master节点", "安装和配置worker节点"]
            varChoice = enquiries.choose("选择操作：", varOptions)

            if varChoice == "安装和配置master节点":
                # 是否设置主机名称
                varSetHostname = "n"
                varHostname = ""
                varHostIp = ""

                varHostname = input("输入hostname（默认k8s-master）： ") or "k8s-master"

                varHostIp = input("输入host ip： ")
                if len(varHostIp.strip()) == 0:
                    raise Exception("必须输入host ip！")

                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_k8s_install.yml"
                if varSetHostname.lower() == "y":
                    var_command = var_command + " -e varSetHostname=true -e varHostname=\"" + varHostname + "\""
                var_command = var_command + " -e varHostIp=\"" + varHostIp + "\""
                var_command = var_command + " -e varMasterNode=true"
                var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser, varHostSshPassword,
                                                        varSudoPassword, varInstallLocally.lower() == "y")
                cli_common.execute_command(var_command)
            else:
                # 是否设置主机名称
                varSetHostname = "n"
                varHostname = ""

                varHostname = input("输入hostname： ")
                if len(varHostname.strip()) == 0:
                    raise Exception("必须输入hostname！")

                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_k8s_install.yml"
                if varSetHostname.lower() == "y":
                    var_command = var_command + " -e varSetHostname=true -e varHostname=\"" + varHostname + "\""
                var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser, varHostSshPassword,
                                                        varSudoPassword, varInstallLocally.lower() == "y")
                cli_common.execute_command(var_command)

            print("提示： -------------------------------------------------------------"
                  "\n在master节点运行kubeadm token create --print-join-command获取加入worker节点命令"
                  "\n在worker节点运行kubeadm join命令加入master节点")
