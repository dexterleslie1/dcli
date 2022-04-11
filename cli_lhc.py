import cli_common
import os
import getpass
import logging


class LhcCli(object):
    """
    lhc管理工具。支持操作系统： centOS8
    """

    def install(self):
        """
        安装lhc

        :return:
        """

        # Full path of python file locates in
        varFullPath = os.path.dirname(os.path.realpath(__file__))

        varInstall = input("是否安装lhc？ [y/n]： ")
        varInstallLocally = "n"

        varHostSshIp = None
        varHostSshUser = None
        varHostSshPassword = ""
        # 是否安装zookeeper
        varInstallZookeeper = "n"
        # 是否安装管理节点单机版redis和数据节点集群版redis
        varInstallRedis = "n"
        # 集群主机ip，创建集群命令redis-cli --cluster create使用
        varRedisClusterBindIp = "127.0.0.1"
        # 是否安装MariaDB
        varInstallMariadb = "n"
        # 是否安装tomcat
        varInstallTomcat = "n"

        if varInstall.lower() == "y":
            varInstallLocally = input("是否本地安装lhc？ [y/n]: ") or "n"
            if not varInstallLocally == "y":
                varHostSshIp = input("安装lhc主机（例如： 192.168.1.20:22）：")
                varHostSshUser = input("安装lhc主机的SSH用户（默认 root）：") or "root"
                varHostSshPassword = getpass.getpass("输入SSH密码：")

            varInstallMariadb = input("是否安装数据库MariaDB？ [y/n]：") or "n"
            varInstallZookeeper = input("是否安装Zookeeper？ [y/n]：") or "n"
            varInstallRedis = input("是否安装管理节点单机版redis和数据节点集群版redis？ [y/n]：") or "n"
            if varInstallRedis.lower() == "y":
                varRedisClusterBindIp = input("redis集群对外提供服务ip（默认：127.0.0.1）：") or "127.0.0.1"
            varInstallTomcat = input("是否安装tomcat？ [y/n]：") or "n"
            if varInstallTomcat.lower() == "y":
                # 判断本地是否有lhcclientmanagement.war、lhcclient.war、lhccronb.war、lhcfacadea.war、lhcfacadez.war、lhcfacaded.war
                varCurrentWorkingDirectory = os.getcwd()
                if not os.path.exists(varCurrentWorkingDirectory + "/lhcclientmanagement.war"):
                    raise Exception("当前工作目录不存在lhcclientmanagement.war文件，不能安装tomcat")
                if not os.path.exists(varCurrentWorkingDirectory + "/lhcclient.war"):
                    raise Exception("当前工作目录不存在lhcclient.war文件，不能安装tomcat")
                if not os.path.exists(varCurrentWorkingDirectory + "/lhccronb.war"):
                    raise Exception("当前工作目录不存在lhccronb.war文件，不能安装tomcat")
                if not os.path.exists(varCurrentWorkingDirectory + "/lhcfacadea.war"):
                    raise Exception("当前工作目录不存在lhcfacadea.war文件，不能安装tomcat")
                if not os.path.exists(varCurrentWorkingDirectory + "/lhcfacadez.war"):
                    raise Exception("当前工作目录不存在lhcfacadez.war文件，不能安装tomcat")
                if not os.path.exists(varCurrentWorkingDirectory + "/lhcfacaded.war"):
                    raise Exception("当前工作目录不存在lhcfacaded.war文件，不能安装tomcat")

        if varInstall.lower() == "y":
            if varInstallLocally.lower() == "y":
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_lhc_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
            else:
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_lhc_install.yml"
                var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                        varHostSshPassword)
            cli_common.execute_command(var_command)

            if varInstallMariadb.lower() == "y":
                if varInstallLocally.lower() == "y":
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_mariadb_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                else:
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_mariadb_install.yml"
                    var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                            varHostSshPassword)
                cli_common.execute_command(var_command)

            if varInstallZookeeper.lower() == "y":
                if varInstallLocally.lower() == "y":
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_zookeeper_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                else:
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_zookeeper_install.yml"
                    var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                            varHostSshPassword)

                var_command = var_command + " -e varPort=2181"

                cli_common.execute_command(var_command)

            if varInstallRedis.lower() == "y":
                # 管理节点单机版redis
                if varInstallLocally.lower() == "y":
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_redis_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                else:
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_redis_install.yml"
                    var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                            varHostSshPassword)

                var_command = var_command + " -e varRedisMode=standalone"

                var_command = var_command + " -e varRedisPort=6379"
                var_command = var_command + " -e varReboot=false"
                var_command = var_command + " -e varRedisPassword=\"123456\""

                cli_common.execute_command(var_command)

                # 数据节点集群版redis
                if varInstallLocally.lower() == "y":
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_redis_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                else:
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_redis_install.yml"
                    var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                            varHostSshPassword)

                var_command = var_command + " -e varRedisMode=cluster -e varAction=clusterCheckRedisClusterFolderExists"
                cli_common.execute_command(var_command)

                varClusterCreateStr = ""
                varClusterNodeCount = 3
                varClusterFirstNodePort = 6380
                for varIndex in range(varClusterNodeCount):
                    logging.info("########################### 部署redis集群第" + str(varIndex+1) + "个节点 ##############################")

                    if varInstallLocally.lower() == "y":
                        var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_redis_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                    else:
                        var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_redis_install.yml"
                        var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                                varHostSshPassword)

                    varClusterNode = "node" + str(varIndex+1)

                    var_command = var_command + " -e varClusterNode=" + varClusterNode
                    var_command = var_command + " -e varRedisMode=cluster"
                    var_command = var_command + " -e varAction=clusterNodeConfig"

                    varClusterNodePort = varClusterFirstNodePort + varIndex
                    var_command = var_command + " -e varClusterNodePort=" + str(varClusterNodePort)

                    cli_common.execute_command(var_command)

                    varClusterCreateStr = varClusterCreateStr + varRedisClusterBindIp + ":" + str(varClusterNodePort)
                    if varIndex < varClusterNodeCount-1:
                        varClusterCreateStr = varClusterCreateStr + " "

                # 调用redis-cli --cluster create创建redis集群
                if varInstallLocally.lower() == "y":
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_redis_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                else:
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_redis_install.yml"
                    var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                            varHostSshPassword)

                var_command = var_command + " -e varReboot=false"

                # https://stackoverflow.com/questions/32584112/ansible-spaces-in-command-line-variables
                var_command = var_command + " -e varRedisMode=cluster -e varAction=clusterCreate -e \"varClusterCreateStr=\'" + varClusterCreateStr + "\'\""
                cli_common.execute_command(var_command)

            if varInstallTomcat.lower() == "y":
                # 安装tomcat-lhc-management
                varTomcatTargetDirectory = "tomcat-lhc-management"
                varTomcatListenPort = 9999
                if varInstallLocally == "y":
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_tomcat_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                else:
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_tomcat_install.yml"
                    var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                            varHostSshPassword)

                var_catalina_opts = "CATALINA_OPTS=\\\"-server"
                var_catalina_opts = var_catalina_opts + " -Xmx1g"

                var_catalina_opts = var_catalina_opts + "\\\""
                var_command = var_command + " -e varCatalinaOpts=\"" + var_catalina_opts + "\""

                var_command = var_command + " -e varTomcatTargetDirectory=" + varTomcatTargetDirectory
                var_command = var_command + " -e varTomcatListenPort=" + str(varTomcatListenPort)
                varTomcatShutdownPort = 8005 + (varTomcatListenPort - 8080)
                var_command = var_command + " -e varTomcatShutdownPort=" + str(varTomcatShutdownPort)

                cli_common.execute_command(var_command)

                # 安装tomcat-lhc-cronb
                varTomcatTargetDirectory = "tomcat-lhc-cronb"
                varTomcatListenPort = 8086
                if varInstallLocally == "y":
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_tomcat_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                else:
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_tomcat_install.yml"
                    var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                            varHostSshPassword)

                var_catalina_opts = "CATALINA_OPTS=\\\"-server"
                var_catalina_opts = var_catalina_opts + " -Xmx1g"

                var_catalina_opts = var_catalina_opts + "\\\""
                var_command = var_command + " -e varCatalinaOpts=\"" + var_catalina_opts + "\""

                var_command = var_command + " -e varTomcatTargetDirectory=" + varTomcatTargetDirectory
                var_command = var_command + " -e varTomcatListenPort=" + str(varTomcatListenPort)
                varTomcatShutdownPort = 8005 + (varTomcatListenPort - 8080)
                var_command = var_command + " -e varTomcatShutdownPort=" + str(varTomcatShutdownPort)

                cli_common.execute_command(var_command)

                # 安装tomcat-lhc-datanode
                varTomcatTargetDirectory = "tomcat-lhc-datanode"
                varTomcatListenPort = 8085
                if varInstallLocally == "y":
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_tomcat_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                else:
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_tomcat_install.yml"
                    var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                            varHostSshPassword)

                var_catalina_opts = "CATALINA_OPTS=\\\"-server"
                var_catalina_opts = var_catalina_opts + " -Xmx1g"

                var_catalina_opts = var_catalina_opts + "\\\""
                var_command = var_command + " -e varCatalinaOpts=\"" + var_catalina_opts + "\""

                var_command = var_command + " -e varTomcatTargetDirectory=" + varTomcatTargetDirectory
                var_command = var_command + " -e varTomcatListenPort=" + str(varTomcatListenPort)
                varTomcatShutdownPort = 8005 + (varTomcatListenPort - 8080)
                var_command = var_command + " -e varTomcatShutdownPort=" + str(varTomcatShutdownPort)

                cli_common.execute_command(var_command)

                # 安装tomcat-lhc-facadea
                varTomcatTargetDirectory = "tomcat-lhc-facadea"
                varTomcatListenPort = 8082
                if varInstallLocally == "y":
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_tomcat_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                else:
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_tomcat_install.yml"
                    var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                            varHostSshPassword)

                var_catalina_opts = "CATALINA_OPTS=\\\"-server"
                var_catalina_opts = var_catalina_opts + " -Xmx1g"

                var_catalina_opts = var_catalina_opts + "\\\""
                var_command = var_command + " -e varCatalinaOpts=\"" + var_catalina_opts + "\""

                var_command = var_command + " -e varTomcatTargetDirectory=" + varTomcatTargetDirectory
                var_command = var_command + " -e varTomcatListenPort=" + str(varTomcatListenPort)
                varTomcatShutdownPort = 8005 + (varTomcatListenPort - 8080)
                var_command = var_command + " -e varTomcatShutdownPort=" + str(varTomcatShutdownPort)

                cli_common.execute_command(var_command)

                # 安装tomcat-lhc-facadez
                varTomcatTargetDirectory = "tomcat-lhc-facadez"
                varTomcatListenPort = 8081
                if varInstallLocally == "y":
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_tomcat_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                else:
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_tomcat_install.yml"
                    var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                            varHostSshPassword)

                var_catalina_opts = "CATALINA_OPTS=\\\"-server"
                var_catalina_opts = var_catalina_opts + " -Xmx1g"

                var_catalina_opts = var_catalina_opts + "\\\""
                var_command = var_command + " -e varCatalinaOpts=\"" + var_catalina_opts + "\""

                var_command = var_command + " -e varTomcatTargetDirectory=" + varTomcatTargetDirectory
                var_command = var_command + " -e varTomcatListenPort=" + str(varTomcatListenPort)
                varTomcatShutdownPort = 8005 + (varTomcatListenPort - 8080)
                var_command = var_command + " -e varTomcatShutdownPort=" + str(varTomcatShutdownPort)

                cli_common.execute_command(var_command)

                # 安装tomcat-lhc-facaded
                varTomcatTargetDirectory = "tomcat-lhc-facaded"
                varTomcatListenPort = 8080
                if varInstallLocally == "y":
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_tomcat_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
                else:
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_tomcat_install.yml"
                    var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser,
                                                            varHostSshPassword)

                var_catalina_opts = "CATALINA_OPTS=\\\"-server"
                var_catalina_opts = var_catalina_opts + " -Xmx1g"

                var_catalina_opts = var_catalina_opts + "\\\""
                var_command = var_command + " -e varCatalinaOpts=\"" + var_catalina_opts + "\""

                var_command = var_command + " -e varTomcatTargetDirectory=" + varTomcatTargetDirectory
                var_command = var_command + " -e varTomcatListenPort=" + str(varTomcatListenPort)
                varTomcatShutdownPort = 8005 + (varTomcatListenPort - 8080)
                var_command = var_command + " -e varTomcatShutdownPort=" + str(varTomcatShutdownPort)

                cli_common.execute_command(var_command)

            print("提醒： lhc所有相关组件已经安装完毕，请导入名为lhcmanagement（管理节点数据库）和lhc（数据节点数据库）数据库后重启操作系统既可访问所有服务")