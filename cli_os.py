import cli_common
import os
import logging
import enquiries
import shutil
import getpass


class OsCli(object):
    """
    操作系统配置管理工具。支持操作系统： centOS8
    """

    def config(self):
        """
        配置操作系统

        :return:
        """

        # 是否关闭系统防火墙
        # 是否关闭系统selinux
        # 是否修改root密码
        # 是否修改ssh端口
        # 是否修改时区为上海
        # 是否配置防止ssh密码暴力破解
        # 是否启用rc.local服务

        varDisableFirewall = "n"
        varDisableSelinux = "n"
        varDisableSwap = "n"
        varChangeRootPassword = "n"
        varNewRootPassword = ""
        varChangeSshPort = "n"
        varNewSshPort = 22
        varChangeTimezone = "n"
        varSshBurstAttackProtection = "n"
        enable_rc_local_service = "n"

        varConfigLocally = "n"
        varHostSshIp = ""
        varHostSshUser = ""
        varHostSshPassword = ""
        varSudoPassword = ""

        varConfigLocally = input("是否本地配置？ [y/n]: ") or "n"
        if not varConfigLocally == "y":
            varHostSshIp = input("编译openresty主机（例如： 192.168.1.20:8080）：")
            varHostSshUser = input("编译openresty主机的SSH用户（默认 root）：") or "root"
            varHostSshPassword = getpass.getpass("输入SSH密码：")

        varSudoPassword = getpass.getpass("输入编译openresty主机的sudo密码，如果当前为root用户不需要输入：")

        varDisableFirewall = input("是否关闭系统防火墙？ [y/n]： ") or "n"
        varDisableSelinux = input("是否关闭系统selinux？ [y/n]： ") or "n"
        varDisableSwap = input("是否关闭系统swap？ [y/n]： ") or "n"
        varChangeRootPassword = input("是否修改root密码？ [y/n]： ") or "n"
        if varChangeRootPassword.lower() == "y":
            varTempRootPassword = getpass.getpass("输入root新密码：")
            varNewRootPassword = getpass.getpass("重复root新密码：")
            if varTempRootPassword != varNewRootPassword:
                raise Exception("输入的两次root密码不一致")

        varChangeSshPort = input("是否修改ssh监听端口？ [y/n]： ") or "n"
        if varChangeSshPort.lower() == "y":
            varNewSshPort = input("输入ssh监听端口（默认值22）：") or 22
            varNewSshPort = int(varNewSshPort)

        varChangeTimezone = input("是否修改时区为上海？ [y/n]：") or "n"
        varSshBurstAttackProtection = input("是否配置防止ssh密码暴力破解？ [y/n]：") or "n"

        enable_rc_local_service = input("是否启用rc.local服务？ [y/n]：") or "n"

        varFullPath = os.path.dirname(os.path.realpath(__file__))

        if varDisableFirewall.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_firewall_install.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser, varHostSshPassword
                                                    , varSudoPassword, varConfigLocally.lower() == "y")
            cli_common.execute_command(var_command)

        if varDisableSelinux.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_selinux_install.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser, varHostSshPassword
                                                    , varSudoPassword, varConfigLocally.lower() == "y")
            cli_common.execute_command(var_command)

        if varDisableSwap.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_os_swap_config.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser, varHostSshPassword
                                                    , varSudoPassword, varConfigLocally.lower() == "y")
            cli_common.execute_command(var_command)

        if varChangeRootPassword.lower() == "y" and len(varChangeRootPassword) > 0:
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_os_root_password_change.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser, varHostSshPassword
                                                    , varSudoPassword, varConfigLocally.lower() == "y")

            var_command = var_command + " -e \"varNewRootPassword=\'" + varNewRootPassword + "\'\""
            cli_common.execute_command(var_command)

        if varChangeSshPort.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_os_ssh_port_change.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser, varHostSshPassword
                                                    , varSudoPassword, varConfigLocally.lower() == "y")

            var_command = var_command + " -e varNewSshPort=" + str(varNewSshPort)
            cli_common.execute_command(var_command)

        if varChangeTimezone.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_os_timezone_change.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser, varHostSshPassword
                                                    , varSudoPassword, varConfigLocally.lower() == "y")
            cli_common.execute_command(var_command)

        if varSshBurstAttackProtection.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_fail2ban_install.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser, varHostSshPassword
                                                    , varSudoPassword, varConfigLocally.lower() == "y")

            var_command = var_command + " -e varEnableSshd=true"

            cli_common.execute_command(var_command)

        if enable_rc_local_service.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_os_rclocal_install.yml"
            var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser, varHostSshPassword
                                                    , varSudoPassword, varConfigLocally.lower() == "y")
            cli_common.execute_command(var_command)

        var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + varFullPath + "/role_os_chrony_install.yml"
        var_command = cli_common.concat_command(var_command, varHostSshIp, varHostSshUser, varHostSshPassword
                                                , varSudoPassword, varConfigLocally.lower() == "y")
        cli_common.execute_command(var_command)

        if enable_rc_local_service.lower() == "y":
            print("启用rc.local服务后通过手动编辑/etc/rc.d/rc.local文件加入开机自启动命令")
