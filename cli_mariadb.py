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
        varMasterReplicationUser = input("Master复制用户（默认值root）：") or "root"
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
        shutil.copyfile(varDefaultConfigFileFullRelativePath + "/mysql-slave-delay-restore.cnf",
                        varCurrentWorkingDirectory + "/mysql-slave-delay-restore.cnf")
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

        varCurrentWorkingDirectory = os.getcwd()
        if not os.path.exists(varCurrentWorkingDirectory + "/.env")\
                or not os.path.exists(varCurrentWorkingDirectory + "/docker-compose.yml"):
            raise Exception("当前所在目录不是数据库备份工作目录，切换到相应的工作目录再重试此命令")

        # 判断当前目录是否存在全量数据库备份
        if not os.path.exists(varCurrentWorkingDirectory + "/fullybackup-restore.tar.gz"):
            raise Exception("当前工作目录不存在名为fullybackup-restore.tar.gz全量数据库备份，无法启动数据库复制")

        # 全新启动需要销毁之前的容器
        varFreshStart = input("是否全新重新启动（注意：全新重新启动会删除之前的实时同步数据后重新开始同步）？ [y/n]: ") or "n"
        if varFreshStart.lower() == "y":
            varCommand = "docker-compose down -v"
            cli_common.execute_command(varCommand)

        varCommand = "docker-compose up -d"
        cli_common.execute_command(varCommand)

        varCommand = "docker-compose logs -f --tail 15"
        cli_common.execute_command(varCommand)

    def slave_status(self):
        """
        查看数据库同步容器状态
        """

        varResult = cli_common.execute_command_by_subprocess_run("docker ps -a")
        varRowList = varResult.stdout.splitlines()
        if len(varRowList) <= 1:
            print("没有相关数据数据库同步容器")
            return

        varRowList = varRowList[1:]
        for item in varRowList:
            varStatusRunning = "Exited" not in item
            varColumnList = item.split()
            varContainerName = varColumnList[len(varColumnList) - 1]
            if varContainerName.startswith("slave-") and not varContainerName.endswith("-auto-config"):
                if not varStatusRunning:
                    print("错误！" + varContainerName + " 数据库同步容器已经Exited停止状态，使用 docker logs " + varContainerName + " 命令查看容器日志分析其中原因")
                else:
                    varCommand = "docker exec " + varContainerName + " mysql -uroot -p123456 -e \"show slave status\G\""
                    varResult = cli_common.execute_command_by_subprocess_run(varCommand)
                    varRowList1 = varResult.stdout.splitlines()
                    varSlaveIORunning = False
                    varSlaveSQLRunning = False
                    varLastErrno = False
                    varLastIOErrno = False
                    varLastSQLErrno = False
                    for item1 in varRowList1:
                        item1 = item1.strip()
                        if item1.startswith("Slave_IO_Running:"):
                            varSlaveIORunning = not item1.endswith("Yes")
                        elif item1.startswith("Slave_SQL_Running:"):
                            varSlaveSQLRunning = not item1.endswith("Yes")
                        elif item1.startswith("Last_Errno:"):
                            varLastErrno = int(item1.split(":")[1].strip()) != 0
                        elif item1.startswith("Last_IO_Errno:"):
                            varLastIOErrno = int(item1.split(":")[1].strip()) != 0
                        elif item1.startswith("Last_SQL_Errno:"):
                            varLastSQLErrno = int(item1.split(":")[1].strip()) != 0

                    if varSlaveIORunning or varSlaveSQLRunning or varLastErrno or varLastIOErrno or varLastSQLErrno:
                        print("错误！" + varContainerName + " 数据库同步容器错误状态，使用 docker exec " + varContainerName + " mysql -uroot -p123456 -e \"show slave status\G\" 查看具体错误原因")
                    else:
                        print("正常。" + varContainerName + " 数据库同步容器正常状态")

    def slave_cleanup(self):
        """
        释放slave-xxxx-auto-config容器
        """

        # 读取所有退出状态容器
        varResult = cli_common.execute_command_by_subprocess_run("docker ps -f \"status=exited\"")
        varRowList = varResult.stdout.splitlines()
        if len(varRowList) <= 1:
            print("没有可清除的容器")
            return

        varRowList = varRowList[1:]
        for item in varRowList:
            varColumnList = item.split()
            varContainerName = varColumnList[len(varColumnList)-1]
            if varContainerName.startswith("slave-") and varContainerName.endswith("-auto-config"):
                cli_common.execute_command_by_subprocess_run("docker rm --force -v " + varContainerName)
                print("成功清除容器 " + varContainerName + " 相关资源")

    def slave_restore_pre(self):
        """
        用于准备数据库恢复容器，原理： 复制delay容器数据到delay restore新容器，之后人工介入还原数据
        """

        varCurrentWorkingDirectory = os.getcwd()

        if not os.path.exists(varCurrentWorkingDirectory + "/.env") \
                or not os.path.exists(varCurrentWorkingDirectory + "/docker-compose.yml"):
            raise Exception("当前所在目录不是数据库备份工作目录，切换到相应的工作目录再重试此命令")

        # 获取项目名称
        varResult = cli_common.execute_command_by_subprocess_run(
            "grep \"varProjectName\" " + varCurrentWorkingDirectory + "/.env | awk -F '=' '{print $2}'")
        varProjectName = varResult.stdout.strip()

        varConfirm = input("是否确定准备项目" + varProjectName + "数据库还原容器吗？ [y/n]: ") or "n"
        if varConfirm.lower() != "y":
            return

        # 停止delay复制同步
        varCommand = "docker exec -it slave-" + varProjectName + "-delay mysql -uroot -p123456 -e \"stop slave\""
        cli_common.execute_command_by_subprocess_run(varCommand)
        print("成功停止 slave-" + varProjectName + "-delay 复制同步线程")

        # 删除之前的slave-xxx-delay-restore容器
        varCommand = "docker rm --force -v slave-" + varProjectName + "-delay-restore || true"
        cli_common.execute_command_by_subprocess_run(varCommand)
        print("成功删除 slave-" + varProjectName + "-delay-restore 容器")

        varVolumeNameRestore = "vol-slave-" + varProjectName + "-delay-restore"

        # 删除之前的restore volume
        varCommand = "docker volume rm " + varVolumeNameRestore + " || true"
        cli_common.execute_command_by_subprocess_run(varCommand)
        print("成功删除 " + varVolumeNameRestore + " 容器数据卷")

        # 使用临时容器复制delay容器数据
        print("准备复制 slave-" + varProjectName + "-delay 容器数据到命名数据卷 " + varVolumeNameRestore + " ，这个过程可能需要等待一段时间。。。")
        varCommand = "docker run --rm -it --volumes-from slave-" + varProjectName + "-delay:ro -v " + varVolumeNameRestore + ":/mount-point-datum centos /bin/sh -c \"rm -rf /mount-point-datum/* && cp -rp /var/lib/mysql/* /mount-point-datum/\""
        cli_common.execute_command_by_subprocess_run(varCommand)
        print("成功复制 slave-" + varProjectName + "-delay 容器数据到命名数据卷 " + varVolumeNameRestore)

        varCommand = "docker run -d --name slave-" + varProjectName + "-delay-restore -e TZ=Asia/Shanghai -v " + varVolumeNameRestore + ":/var/lib/mysql -v " + varCurrentWorkingDirectory + "/mysql-slave-delay-restore.cnf:/etc/mysql/conf.d/my.cnf mariadb:10.4.19"
        cli_common.execute_command_by_subprocess_run(varCommand)
        print("成功创建数据还原容器 slave-" + varProjectName + "-delay-restore")

        print("成功从容器 slave-" + varProjectName + "-delay 复制数据到容器 slave-" + varProjectName + "-delay-restore 中，" +
              "使用 docker exec -it slave-" + varProjectName + "-delay-restore /bin/bash 进入并还原数据，具体数据还原步骤参照当前工作目录的README.md文件")

    def slave_export(self):
        """
        容器数据还原后使用这个命令导出数据用于数据还原
        """

        varCurrentWorkingDirectory = os.getcwd()

        if not os.path.exists(varCurrentWorkingDirectory + "/.env") \
                or not os.path.exists(varCurrentWorkingDirectory + "/docker-compose.yml"):
            raise Exception("当前所在目录不是数据库备份工作目录，切换到相应的工作目录再重试此命令")

        # 获取项目名称
        varResult = cli_common.execute_command_by_subprocess_run(
            "grep \"varProjectName\" " + varCurrentWorkingDirectory + "/.env | awk -F '=' '{print $2}'")
        varProjectName = varResult.stdout.strip()

        varResult = cli_common.execute_command_by_subprocess_run(
            "grep \"varMasterDatabaseName\" " + varCurrentWorkingDirectory + "/.env | awk -F '=' '{print $2}'")
        varMasterDatabaseName = varResult.stdout.strip()

        varConfirm = input("是否确定导出项目" + varProjectName + "还原后的数据吗？ [y/n]: ") or "n"
        if varConfirm.lower() != "y":
            return

        print("准备导出还原后的数据，可能需要等待一段时间。。。")
        varCommand = "docker exec -it slave-hm2015-delay-restore mysqldump -uroot -p123456 --single-transaction --quick --lock-tables=false " + varMasterDatabaseName + " | gzip -c > restore-export.gz"
        cli_common.execute_command_by_subprocess_run(varCommand)
        print("成功导出还原后的数据到当前工作目录的数据文件 restore-export.gz，使用命令 gzip -dkc restore-export.gz > restore-export.sql 解压数据到restore-export.sql文件")
