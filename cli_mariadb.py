import cli_common
import os
import getpass
import shutil


class MariadbCli(object):
    """
    MariaDB管理工具。支持操作系统： centOS8
    """

    def install(self):
        """
        安装MariaDB

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        varHostMariadbIp = ""
        varHostMariadbUser = ""
        varHostMariadbPassword = ""
        varInstallLocally = "n"

        varInstall = input("是否安装MariaDB？ [y/n]: ")
        if varInstall.lower() == "y":
            varInstallLocally = input("是否本地安装？ [y/n]: ") or "n"

            if not varInstallLocally.lower() == "y":
                varHostMariadbIp = input("输入目标主机IP（例如： 192.168.1.20:8080）：")
                varHostMariadbUser = input("输入目标主机SSH用户（默认 root）：") or "root"
                varHostMariadbPassword = getpass.getpass("输入SSH密码：")

        if varInstall.lower() == "y":
            if varInstallLocally.lower() == "y":
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_mariadb_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
            else:
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_mariadb_install.yml"
                var_command = cli_common.concat_command(var_command, varHostMariadbIp, varHostMariadbUser, varHostMariadbPassword)
            cli_common.execute_command(var_command)

    def slave_config(self):
        """
        在当前工作目录生成slave的相关配置文件，具体操作步骤参考当前工作目录的README.md文件

        :return:
        """

        varConfig = input("是否确定在当前目录生成slave相关配置？ [y/n]: ") or "n"
        if varConfig.lower() != "y":
            return

        # 判断当前工作目录是否为空
        varCurrentWorkingDirectory = os.getcwd()
        if os.path.exists(varCurrentWorkingDirectory + "/.env"):
            raise Exception("当前工作目录不为空目录，不能创建slave相关配置文件")

        varProjectName = ""
        varMasterDatabaseName = ""
        varMasterIp = ""
        varMasterPort = 3306
        varMasterReplicationUser = ""
        varMasterReplicationUserPassword = ""
        varRecompileSlaveAutoConfigDockerImage = "n"

        # 询问是否重新编译slave-auto-config docker镜像
        varRecompileSlaveAutoConfigDockerImage = input("是否重新编译slave-auto-config镜像？ [y/n]: ") or "n"

        # 询问项目名称，例如：hm2015、hm2016等
        varProjectName = input("当前项目名称，例如：hm2015、hm2016等： ")
        if varProjectName.strip() == "":
            raise Exception("没有指定前项目名称")

        # 询问master数据库名称
        varMasterDatabaseName = input("Master数据库名称： ")
        if varMasterDatabaseName.strip() == "":
            raise Exception("没有指定Master数据库名称")

        # 询问master ip地址
        varMasterIp = input("Master ip地址：")
        if varMasterIp.strip() == "":
            raise Exception("没有指定Master ip地址")

        # 询问master端口
        varMasterPort = input("Master端口（默认值3306）：") or 3306
        varMasterPort = int(varMasterPort)
        if varMasterPort <= 0:
            raise Exception("没有指定Master端口")

        # 询问master复制用户
        varMasterReplicationUser = input("Master复制用户：")
        if varMasterReplicationUser.strip() == "":
            raise Exception("没有指定Master复制用户")

        # 询问master复制用户的密码
        varMasterReplicationUserPassword = getpass.getpass("Master复制用户的密码：")
        if varMasterReplicationUserPassword.strip() == "":
            raise Exception("没有指定Master复制用户的密码")

        varSudoPassword = getpass.getpass("输入当前主机的sudo密码，如果当前为root用户不需要输入：")

        # 复制.env.template
        varFullPath = os.path.dirname(os.path.realpath(__file__))
        var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_mariadb_slave_config.yml"
        var_command = cli_common.concat_command(var_command, "", "", "", varSudoPassword, True)
        var_command = var_command + " -e varProjectName=" + varProjectName
        var_command = var_command + " -e varMasterDatabaseName=" + varMasterDatabaseName
        var_command = var_command + " -e varMasterIp=" + varMasterIp
        var_command = var_command + " -e varMasterPort=" + str(varMasterPort)
        var_command = var_command + " -e varMasterReplicationUser=" + varMasterReplicationUser
        var_command = var_command + " -e varMasterReplicationUserPassword=" + varMasterReplicationUserPassword
        var_command = var_command + " -e varSrcTemplate=.env.template"
        var_command = var_command + " -e varDestTemplate=\"" + varCurrentWorkingDirectory + "/.env\""
        var_command = var_command + " -e varCopyTemplate=True"
        cli_common.execute_command(var_command)

        varExecutionDirection = os.path.dirname(os.path.realpath(__file__))
        varDefaultConfigFileFullRelativePath = varExecutionDirection + "/role_mariadb_slave_config/files"
        # 复制docker-compose.yml
        var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_mariadb_slave_config.yml"
        var_command = cli_common.concat_command(var_command, "", "", "", varSudoPassword, True)
        var_command = var_command + " -e varProjectName=" + varProjectName
        var_command = var_command + " -e varSrcTemplate=docker-compose.yml.template"
        var_command = var_command + " -e varDestTemplate=\"" + varCurrentWorkingDirectory + "/docker-compose.yml\""
        var_command = var_command + " -e varCopyTemplate=True"
        cli_common.execute_command(var_command)

        # 复制docker-slave-auto-config.sh
        shutil.copyfile(varDefaultConfigFileFullRelativePath + "/docker-slave-auto-config.sh",
                        varCurrentWorkingDirectory + "/docker-slave-auto-config.sh")
        # 复制Dockerfile-slave-auto-config
        shutil.copyfile(varDefaultConfigFileFullRelativePath + "/Dockerfile-slave-auto-config",
                        varCurrentWorkingDirectory + "/Dockerfile")
        # 复制mysql-slave.cnf
        shutil.copyfile(varDefaultConfigFileFullRelativePath + "/mysql-slave-live.cnf",
                        varCurrentWorkingDirectory + "/mysql-slave-live.cnf")
        shutil.copyfile(varDefaultConfigFileFullRelativePath + "/mysql-slave-delay.cnf",
                        varCurrentWorkingDirectory + "/mysql-slave-delay.cnf")
        # 复制README.md文件到当前工作目录
        shutil.copyfile(varDefaultConfigFileFullRelativePath + "/README.md",
                        varCurrentWorkingDirectory + "/README.md")

        if varRecompileSlaveAutoConfigDockerImage.lower() == "y":
            var_command = "docker build --tag docker.118899.net:10001/yyd-public/slave-auto-config --file Dockerfile " + varCurrentWorkingDirectory
            cli_common.execute_command(var_command)

    def slave_start(self):
        """
        启动数据库复制

        :return:
        """

        varStart = input("是否确定启动/重新启动数据库复制吗？ [y/n]: ") or "n"
        if varStart.lower() != "y":
            return

        # 判断当前目录是否存在全量数据库备份
        varCurrentWorkingDirectory = os.getcwd()
        if not os.path.exists(varCurrentWorkingDirectory + "/fullybackup-restore.tar.gz"):
            raise Exception("当前工作目录不存在名为fullybackup-restore.tar.gz全量数据库备份，无法启动数据库复制")

        # 全新启动需要销毁之前的容器
        varFreshStart = input("是否全新重新启动（注意：全新重新启动会删除之前的实时同步数据后重新开始同步）？ [y/n]: ") or "n"
        if varFreshStart.lower() == "y":
            varCommand = "docker-compose down"
            cli_common.execute_command(varCommand)

        varCommand = "docker-compose up -d"
        cli_common.execute_command(varCommand)

        varCommand = "docker-compose logs -f"
        cli_common.execute_command(varCommand)

    def slave_status(self):
        """

        """

        # todo 自动遍历当前工作目录