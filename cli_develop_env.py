import cli_common
import os


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

        var_install_locally = input("是否本地安装？ [y/n]: ") or "n"
        if not var_install_locally == "y":
            var_host_target = input("目标主机（例如： 192.168.1.20:8080）：")
            var_host_target_user = input("目标主机SSH用户（默认 root）：") or "root"

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        if var_install_locally == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_develop_env_install.yml --ask-become-pass --connection=local -i 127.0.0.1,"
        else:
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_develop_env_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target, var_host_target_user)

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
            # 当安装Jmeter时，提示输入Jmeter -Xmx内存值
            var_heap_mx = input("输入Jmeter最大java堆内存，单位GB（默认1GB）：") or "1"
            var_command = var_command + " -e var_heap_mx=" + var_heap_mx

        cli_common.execute_command(var_command)
