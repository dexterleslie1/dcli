import cli_common
import os
import logging
import enquiries
import shutil
import getpass


class OpenrestyCli(object):
    """
    openresty管理工具。支持操作系统： centOS8
    """

    def install(self, from_source=True):
        """
        安装openresty

        :param from_source:
            true 从源代码安装openresty，需要指定编译openresty主机。
            false 从yum安装openresty。
        :return:
        """

        # openresty是frontend还是backend
        varFrontend = True

        # 获取当前工作目录
        varCurrentWorkingDirectory = os.getcwd()

        # 询问用户是安装部署openresty还是在当前工作目录生成default.conf和naxsi.rules模板
        varOptions = ["在当前目录生成default.conf和naxsi.rules模板", "安装部署"]
        varChoice = enquiries.choose("选择操作：", varOptions)

        if varChoice == "在当前目录生成default.conf和naxsi.rules模板":
            # 判断当前目录是否已经存在default.conf和naxsi.rules模板
            # 是则提示用户并且不生成default.conf和naxsi.rules模板
            # 否则就生成default.conf和naxsi.rules模板
            if os.path.exists(varCurrentWorkingDirectory + "/default.conf"):
                raise Exception("当前工作目录已经存在名为default.conf文件，不能在当前目录生成defaut.conf模板文件")
            if os.path.exists(varCurrentWorkingDirectory + "/naxsi.rules"):
                raise Exception("当前工作目录已经存在名为naxsi.rules文件，不能在当前目录生成naxsi.rules模板文件")

            # 询问用户是安装部署frontend openrety还是backend openresty
            varOptions = ["frontend", "backend"]
            varChoice = enquiries.choose("安装部署frontend（用户使用浏览器直接访问的openresty）还是backend（代理后端tomcat的openresty） openresty：", varOptions)

            varDefaultConfigTemplate = "default.conf.backend.template"
            if varChoice == "frontend":
                varDefaultConfigTemplate = "default.conf.frontend.template"

            # 复制default.conf和naxsi.rules模板文件到当前工作目录
            varExecutionDirection = os.path.dirname(os.path.realpath(__file__))
            varDefaultConfigTemplateFullRelativePath = varExecutionDirection + "/role_openresty_install/templates/" + varDefaultConfigTemplate
            shutil.copyfile(varDefaultConfigTemplateFullRelativePath, varCurrentWorkingDirectory + "/default.conf")

            if varChoice != "frontend":
                shutil.copyfile(varExecutionDirection + "/role_openresty_install/templates/naxsi.rules.template", varCurrentWorkingDirectory + "/naxsi.rules")
            print("提示： 成功在当前工作目录生成default.conf和naxsi.rules模板文件，可以通过编辑default.conf和naxsi.rules自定义openresty配置")

        else:
            # 判断当前工作目录是否存在default.conf文件，否则报错提示用户先使用“在当前目录生成default.conf和naxsi.rules模板”生成相关模板
            if not os.path.exists(varCurrentWorkingDirectory + "/default.conf"):
                raise Exception("当前工作目录不存在default.conf文件，先使用“在当前目录生成default.conf和naxsi.rules模板”生成相关模板配置")

            # Full path of python file locates in
            var_full_path = os.path.dirname(os.path.realpath(__file__))

            var_compile_locally = "n"
            var_install_locally = "n"
            varCompileHostSshIp = ""
            varCompileHostSshUser = ""
            varCompileHostSshPassword = ""
            varDeploymentHostSshIp = ""
            varDeploymentHostSshUser = ""
            varDeploymentHostSshPassword = ""
            varSudoPasswordCompile = ""
            varSudoPasswordDeployment = ""

            if from_source:
                var_compile = input("是否编译openresty？ [y/n]： ")
                var_install = input("安装openresty？ [y/n]： ")
                if var_compile.lower() == "y":
                    var_compile_locally = input("是否本地编译openresty？ [y/n]: ") or "n"
                    if not var_compile_locally == "y":
                        varCompileHostSshIp = input("编译openresty主机（例如： 192.168.1.20:8080）：")
                        varCompileHostSshUser = input("编译openresty主机的SSH用户（默认 root）：") or "root"
                        varCompileHostSshPassword = getpass.getpass("输入SSH密码：")

                    varSudoPasswordCompile = getpass.getpass("输入编译openresty主机的sudo密码，如果当前为root用户不需要输入：")

                if var_install.lower() == "y":
                    # 询问用户是安装部署frontend openrety还是backend openresty
                    varOptions = ["frontend", "backend"]
                    varChoice = enquiries.choose(
                        "安装部署frontend（用户使用浏览器直接访问的openresty）还是backend（代理后端tomcat的openresty） openresty：", varOptions)
                    if varChoice == "frontend":
                        varFrontend = True
                    else:
                        varFrontend = False

                    var_install_locally = input("是否本地部署openresty？ [y/n]: ") or "n"
                    if not var_install_locally == "y":
                        varDeploymentHostSshIp = input("部署openresty主机（例如： 192.168.1.20:8080）：")
                        varDeploymentHostSshUser = input("部署openresty主机的SSH用户（默认 root）：") or "root"
                        varDeploymentHostSshPassword = getpass.getpass("输入SSH密码：")

                    varSudoPasswordDeployment = getpass.getpass("输入部署openresty主机的sudo密码，如果当前为root用户不需要输入：")

                if var_compile.lower() == "y":
                    # 在编译主机中编译openresty
                    logging.info("########################### 编译openresty ##############################")

                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_openresty_compile.yml"
                    var_command = cli_common.concat_command(var_command, varCompileHostSshIp, varCompileHostSshUser, varCompileHostSshPassword
                                                            , varSudoPasswordCompile, var_compile_locally.lower() == "y")
                    cli_common.execute_command(var_command)

                if var_install.lower() == "y":
                    # 部署openresty
                    logging.info("########################### 部署openresty ##############################")

                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_openresty_install.yml"
                    var_command = cli_common.concat_command(var_command, varDeploymentHostSshIp, varDeploymentHostSshUser, varDeploymentHostSshPassword
                                                            , varSudoPasswordDeployment, var_install_locally.lower() == "y")

                    var_command = var_command + " -e varCurrentWorkingDirectory=\"" + varCurrentWorkingDirectory + "\""

                    if varFrontend:
                        var_command = var_command + " -e varFrontend=true"
                    else:
                        var_command = var_command + " -e varBackend=true"

                    cli_common.execute_command(var_command)

                    # 安装配置fail2ban服务
                    var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_fail2ban_install.yml"
                    var_command = cli_common.concat_command(var_command, varDeploymentHostSshIp, varDeploymentHostSshUser, varDeploymentHostSshPassword
                                                            , varSudoPasswordDeployment, var_install_locally.lower() == "y")

                    if varFrontend:
                        var_command = var_command + " -e varFrontend=true"
                    else:
                        var_command = var_command + " -e varBackend=true"
                    cli_common.execute_command(var_command)

                    print("提示： 已经成功安装配置openresty和fail2ban，需要手动重启操作系统使内核性能优化参数生效。")
            else:
                # TODO: Install openresty from yum repository
                raise Exception("Install openresty from yum repository not implement yet.")