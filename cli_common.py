import subprocess
import logging


def execute_command(command):
    logging.info("Prepare to execute command '" + command + "'")
    var_result = subprocess.call(command, shell=True)
    if var_result != 0:
        raise Exception, "Run command '" + command + "' failed"


def concat_command(command, remote_hosts, remote_user):
    if remote_hosts:
        if not remote_hosts.endswith(","):
            remote_hosts = remote_hosts + ","
        command = command + " --inventory " + remote_hosts
    if remote_user:
        command = command + " --user " + remote_user

    command = command + " --ask-pass"
    return command
