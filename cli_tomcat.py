import cli_common
import os
import getpass


class TomcatCli(object):
    """
    tomcat管理工具。支持操作系统： centOS8
    """

    def install(self):
        """
        安装tomcat

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_install = input("是否安装tomcat？ [y/n]： ")
        var_install_locally = "n"

        var_host_target = None
        var_host_target_user = None
        varHostSshPassword = ""

        var_xmx = None
        var_xmx_setting = "n"
        var_jmx_enable = "n"
        var_jmx_host = None
        var_jmx_port = None
        varTomcatTargetDirectory = "tomcat"
        varTomcatListenPort = 8080
        varTomcatShutdownPort = 8005

        if var_install.lower() == "y":
            var_install_locally = input("是否本地安装tomcat？ [y/n]: ") or "n"
            if not var_install_locally == "y":
                var_host_target = input("安装tomcat主机（例如： 192.168.1.20:22）：")
                var_host_target_user = input("安装tomcat主机的SSH用户（默认 root）：") or "root"
                varHostSshPassword = getpass.getpass("输入SSH密码：")

            # 部署的tomcat目录名称
            varTomcatTargetDirectory = input("设置tomcat部署目录（默认tomcat）：") or "tomcat"

            # 设置tomcat监听端口
            varTomcatListenPort = input("设置tomcat监听端口（默认8080）：") or 8080
            varTomcatListenPort = int(varTomcatListenPort)
            varTomcatShutdownPort = 8005 + (varTomcatListenPort - 8080)

            # 设置tomcat xmx内存
            var_xmx_setting = input("是否设置tomcat xmx？[y/n]：") or "n"
            if var_xmx_setting.lower() == "y":
                var_xmx = input("输入tomcat xmx内存设置值，单位GB。（默认值：1GB）：") or "1"

            # 是否启用jmx
            var_jmx_enable = input("是否启用tomcat jmx设置？[y/n]：") or "n"
            if var_jmx_enable.lower() == "y":
                var_jmx_host = input("输入tomcat jmx主机IP（例如：192.168.1.1，默认值：127.0.0.1）：") or "127.0.0.1"
                var_jmx_port = input("输入tomcat jmx监听端口（例如：18999，默认值：18999）：") or "18999"

        if var_install.lower() == "y":
            if var_install_locally == "y":
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_tomcat_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
            else:
                var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_tomcat_install.yml"
                var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user, varHostSshPassword)

            if var_xmx_setting.lower() == "y" or var_jmx_enable.lower() == "y":
                var_catalina_opts = "CATALINA_OPTS=\\\"-server"
                if var_xmx_setting.lower() == "y" and var_xmx is not None:
                    var_catalina_opts = var_catalina_opts + " -Xmx" + var_xmx + "g"
                if var_jmx_enable.lower() == "y":
                    var_catalina_opts = var_catalina_opts + " -Djava.rmi.server.hostname=" + var_jmx_host
                    var_catalina_opts = var_catalina_opts + " -Dcom.sun.management.jmxremote.port=" + var_jmx_port
                    var_catalina_opts = var_catalina_opts + " -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false"

                var_catalina_opts = var_catalina_opts + "\\\""
                var_command = var_command + " -e varCatalinaOpts=\"" + var_catalina_opts + "\""

            var_command = var_command + " -e varTomcatTargetDirectory=" + varTomcatTargetDirectory
            var_command = var_command + " -e varTomcatListenPort=" + str(varTomcatListenPort)
            var_command = var_command + " -e varTomcatShutdownPort=" + str(varTomcatShutdownPort)

            cli_common.execute_command(var_command)