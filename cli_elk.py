import cli_common
import os


class ElkCli(object):
    """
    Cli for managing elasticsearch, logstash, kibana. OS support: centOS8
    """

    def install(self):
        """
        Install elasticsearch, logstash, kibana.
        Access http://localhost:9200 for determining if getting elasticsearch installed successfully.
        Access http://localhost:5601 for determining if getting kibana installed successfully.

        :return:
        """

        # Full path of python file locates in
        var_full_path = os.path.dirname(os.path.realpath(__file__))

        var_install = raw_input("Install Elasticsearch? [y/n]: ")
        if var_install.lower() == "y":
            var_host_target_elasticsearch = raw_input("Enter deploying target machine (example: 192.168.1.20:8080): ")
            var_host_target_user_elasticsearch = raw_input("Enter target machine user (default root): ") or "root"
        var_install_logstash = raw_input("Install Logstash? [y/n]: ")
        if var_install_logstash.lower() == "y":
            var_host_target_logstash = raw_input("Enter deploying target machine (example: 192.168.1.20:8080): ")
            var_host_target_user_logstash = raw_input("Enter target machine user (default root): ") or "root"
        var_install_kibana = raw_input("Install kibana? [y/n]: ")
        if var_install_kibana.lower() == "y":
            var_host_target_kibana = raw_input("Enter deploying target machine (example: 192.168.1.20:8080): ")
            var_host_target_user_kibana = raw_input("Enter target machine user (default root): ") or "root"

        if var_install.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_elasticsearch_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target_elasticsearch, var_host_target_user_elasticsearch)
            cli_common.execute_command(var_command)

        if var_install_logstash.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_logstash_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target_logstash, var_host_target_user_logstash)
            cli_common.execute_command(var_command)

        if var_install_kibana.lower() == "y":
            var_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook " + var_full_path + "/role_kibana_install.yml"
            var_command = cli_common.concat_command(var_command, var_host_target_kibana, var_host_target_user_kibana)
            cli_common.execute_command(var_command)