import cli_common
import os
import getpass
import enquiries
import logging


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
        varRedisMode = ""
        varInstallLocally = "n"
        varSudoPassword = ""
        varReboot  = "n"

        # redis集群节点数
        varClusterNodeCount = 3
        varClusterFirstNodePort = 6379
        varClusterBindIp = "127.0.0.0"

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
                # 集群节点数
                varClusterNodeCount = input("redis集群节点数（注意：集群节点数不能小于3，默认值：3）：") or 3
                varClusterNodeCount = int(varClusterNodeCount)
                if varClusterNodeCount < 3:
                    varClusterNodeCount = 3
                # 集群第一个节点端口，之后节点端口+1
                varClusterFirstNodePort = input("redis集群第一个节点监听端口（说明：第一个节点监听6379端口，第二个节点监听6380端口，如此类推，默认值：6379）：") or 6379
                varClusterFirstNodePort = int(varClusterFirstNodePort)
                # 集群主机ip，创建集群命令redis-cli --cluster create使用
                varClusterBindIp = input("redis集群对外提供服务ip（默认：127.0.0.1）：") or "127.0.0.1"

            varInstallLocally = input("是否本地安装？ [y/n]: ") or "n"

            if not varInstallLocally.lower() == "y":
                varHostRedisIp = input("输入目标主机IP（例如： 192.168.1.20:8080）：")
                varHostRedisUser = input("输入目标主机SSH用户（默认 root）：") or "root"
                varHostRedisPassword = getpass.getpass("输入SSH密码：")

            varSudoPassword = getpass.getpass("输入主机的sudo密码，如果当前为root用户不需要输入：")

        if varInstall.lower() == "y":
            if varRedisMode == "单机版":
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_redis_install.yml"
                var_command = cli_common.concat_command(var_command, varHostRedisIp, varHostRedisUser, varHostRedisPassword,
                                                        varSudoPassword, varInstallLocally.lower() == "y")

                cli_common.execute_command(var_command)

                var_command = var_command + " -e varRedisMode=standalone"

                if len(varRedisPort) > 0:
                    var_command = var_command + " -e varRedisPort=" + varRedisPort

                if varReboot.lower() == "y":
                    var_command = var_command + " -e varReboot=true"
                else:
                    var_command = var_command + " -e varReboot=false"

                if len(varRedisPassword) > 0:
                    var_command = var_command + " -e varRedisPassword=\"" + varRedisPassword + "\""

                cli_common.execute_command(var_command)
            else:
                # redis集群判断/data/redis-cluster目录是否已经存在
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_redis_install.yml"
                var_command = cli_common.concat_command(var_command, varHostRedisIp, varHostRedisUser,
                                                        varHostRedisPassword,
                                                        varSudoPassword, varInstallLocally.lower() == "y")
                var_command = var_command + " -e varRedisMode=cluster -e varAction=clusterCheckRedisClusterFolderExists"
                cli_common.execute_command(var_command)

                varClusterCreateStr = ""
                for varIndex in range(varClusterNodeCount):
                    logging.info("########################### 部署redis集群第" + str(varIndex+1) + "个节点 ##############################")

                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_redis_install.yml"
                    var_command = cli_common.concat_command(var_command, varHostRedisIp, varHostRedisUser,
                                                            varHostRedisPassword,
                                                            varSudoPassword, varInstallLocally.lower() == "y")

                    varClusterNode = "node" + str(varIndex+1)

                    var_command = var_command + " -e varClusterNode=" + varClusterNode
                    var_command = var_command + " -e varRedisMode=cluster"
                    var_command = var_command + " -e varAction=clusterNodeConfig"

                    varClusterNodePort = varClusterFirstNodePort + varIndex
                    var_command = var_command + " -e varClusterNodePort=" + str(varClusterNodePort)

                    cli_common.execute_command(var_command)

                    varClusterCreateStr = varClusterCreateStr + varClusterBindIp + ":" + str(varClusterNodePort)
                    if varIndex < varClusterNodeCount-1:
                        varClusterCreateStr = varClusterCreateStr + " "

                # 调用redis-cli --cluster create创建redis集群
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_redis_install.yml"
                var_command = cli_common.concat_command(var_command, varHostRedisIp, varHostRedisUser,
                                                        varHostRedisPassword,
                                                        varSudoPassword, varInstallLocally.lower() == "y")

                if varReboot.lower() == "y":
                    var_command = var_command + " -e varReboot=true"
                else:
                    var_command = var_command + " -e varReboot=false"

                # https://stackoverflow.com/questions/32584112/ansible-spaces-in-command-line-variables
                var_command = var_command + " -e varRedisMode=cluster -e varAction=clusterCreate -e \"varClusterCreateStr=\'" + varClusterCreateStr + "\'\""
                cli_common.execute_command(var_command)