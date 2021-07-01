import cli_common
import os


class KamailioCli(object):
    """
    Cli for managing kamailio. OS support: Debian10
    """

    def install(self):
        """
        Call ansible role_kamailio_install role to install kamailio.

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_install_kamailio = raw_input("Install Kamailio? [y/n]: ")
        if var_install_kamailio.lower() == "y":
            var_host_target_kamailio = raw_input("Enter deploying target machine (example: 192.168.1.20:8080): ")
            var_host_target_user_kamailio = raw_input("Enter target machine user (default root): ") or "root"
        var_install_rtpengine = raw_input("Install Rtpengine? [y/n]: ")
        if var_install_rtpengine.lower() == "y":
            var_host_target_rtpengine = raw_input("Enter deploying target machine (example: 192.168.1.20:8080): ")
            var_host_target_user_rtpengine = raw_input("Enter target machine user (default root): ") or "root"

        if var_install_kamailio.lower() == "y" or var_install_rtpengine.lower() == "y":
            var_external_kamailio_ip = raw_input("Enter kamailio external ip: ")
            var_internal_kamailio_ip = raw_input("Enter kamailio internal ip: ")

        if var_install_kamailio.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_kamailio_install.yml -e 'ansible_python_interpreter=/usr/bin/python3'"
            var_command = cli_common.concat_command(var_command, var_host_target_kamailio, var_host_target_user_kamailio)
            if var_external_kamailio_ip:
                var_command = var_command + " -e var_external_kamailio_ip=" + var_external_kamailio_ip
            if var_internal_kamailio_ip:
                var_command = var_command + " -e var_internal_kamailio_ip=" + var_internal_kamailio_ip
            cli_common.execute_command(var_command)

        if var_install_rtpengine.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_rtpengine_install.yml -e 'ansible_python_interpreter=/usr/bin/python3'"
            var_command = cli_common.concat_command(var_command, var_host_target_rtpengine, var_host_target_user_rtpengine)
            if var_external_kamailio_ip:
                var_command = var_command + " -e var_external_kamailio_ip=" + var_external_kamailio_ip
            if var_internal_kamailio_ip:
                var_command = var_command + " -e var_internal_kamailio_ip=" + var_internal_kamailio_ip
            cli_common.execute_command(var_command)