import subprocess
import logging


def execute_command(command):
    logging.info("Prepare to execute command '" + command + "'")
    var_result = subprocess.call(command, shell=True)
    if var_result != 0:
        raise Exception("Run command '" + command + "' failed")


def concat_command(command, remote_hosts, remote_user, remotePassword = None, sudoPassword = None, installLocally = False):
    if remotePassword is None:
        if remote_hosts:
            if not remote_hosts.endswith(","):
                remote_hosts = remote_hosts + ","
            command = command + " --inventory " + remote_hosts
        if remote_user:
            command = command + " --user " + remote_user

        command = command + " --ask-pass"
    else:
        if remote_hosts:
            if not remote_hosts.endswith(","):
                remote_hosts = remote_hosts + ","
            command = command + " --inventory " + remote_hosts
        if remote_user:
            command = command + " --user " + remote_user

        # https://stackoverflow.com/questions/41771725/ansible-2-1-2-playbook-pass-ssh-password-and-sudo-password-as-command-line-args
        # command = command + "-e \"ansible_user=username ansible_ssh_pass=xxx ansible_sudo_pass=xxx\""
        command = command + " -e \"ansible_ssh_pass=" + remotePassword + "\""

    if sudoPassword is not None:
        command = command + " -e \"ansible_sudo_pass=" + sudoPassword + "\""

    if installLocally:
        command = command + " --connection=local -i 127.0.0.1,"

    return command
