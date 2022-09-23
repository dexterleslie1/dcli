import cli_common
import os
import enquiries
import getpass


class DevelopEnvCli(object):
    """
    开发环境配置管理工具，详细参数支持使用dcli develop_env install --help查看，例如安装Jemter： dcli develop_env install --include_jmeter=true。支持操作系统： centOS8
    """

    def install(self,
                include_jdk=False,
                include_git=False,
                include_maven=False,
                include_mariadb=False,
                include_redis=False,
                include_intellij=False,
                include_smartgit=False,
                include_xrdp=False,
                include_jmeter=False):
        """
        Install develop environment.

        :param remote_hosts
        :param remote_user
        :return:
        """

        var_host_target = ""
        var_host_target_user = ""
        varHostSshPassword = ""
        varSudoPassword = ""

        var_install_locally = input("是否本地安装？ [y/n]: ") or "n"
        if not var_install_locally == "y":
            var_host_target = input("目标主机（例如： 192.168.1.20:8080）：")
            var_host_target_user = input("目标主机SSH用户（默认 root）：") or "root"
            varHostSshPassword = getpass.getpass("输入SSH密码：")

        varSudoPassword = getpass.getpass("输入主机的sudo密码，如果当前为root用户不需要输入：")

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_develop_env_install.yml"
        var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user
                                                    , varHostSshPassword, varSudoPassword, var_install_locally.lower() == "y")

        if include_jdk:
            var_command = var_command + " -e var_include_jdk=true"
        if include_git:
            var_command = var_command + " -e var_include_git=true"
        if include_maven:
            var_command = var_command + " -e var_include_maven=true"
        if include_mariadb:
            var_command = var_command + " -e var_include_mariadb=true"
        if include_redis:
            var_command = var_command + " -e var_include_redis=true"
        if include_intellij:
            var_command = var_command + " -e var_include_intellij=true"
        if include_smartgit:
            var_command = var_command + " -e var_include_smartgit=true"
        if include_xrdp:
            var_command = var_command + " -e var_include_xrdp=true"
        if include_jmeter:
            var_command = var_command + " -e var_include_jmeter=true"
            if not include_jdk:
                var_command = var_command + " -e var_include_jdk=true"

            varOptions = ["master模式", "slave模式"]
            varChoice = enquiries.choose("选择Jmeter安装和配置模式：", varOptions)

            if varChoice == "master模式":
                var_remote_hosts = input("输入jmeter.properties remote_hosts设置（例如：192.168.1.1,192.168.1.2，多个主机之间用逗号分开）：")

                var_command = var_command + " -e varRemoteHosts=" + var_remote_hosts
                var_command = var_command + " -e varMasterMode=true"
            else:
                var_rmi_listen_ip = input("* 输入Jmeter slave模式rmi监听的ip地址：")

                if len(var_rmi_listen_ip.strip()) == 0:
                    raise Exception("必须输入Jmeter slave模式rmi监听的ip地址！")

                var_command = var_command + " -e varRmiListenIp=" + var_rmi_listen_ip
                var_command = var_command + " -e var_slave_mode=true"

            # 当安装Jmeter时，提示输入Jmeter -Xmx内存值
            var_heap_mx = input("输入Jmeter最大java堆内存，单位GB（默认1GB）：") or 1
            var_heap_mx = int(var_heap_mx)
            var_command = var_command + " -e var_heap_mx=" + str(var_heap_mx)

        cli_common.execute_command(var_command)

        if include_intellij:
            print("intellij idea破解文件jetbrains-agent.jar已经下载到当前用户目录/home中，打开idea后直接拖动此文件到序列号提示框即可破解")
