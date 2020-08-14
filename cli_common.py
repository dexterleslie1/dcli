import subprocess


def execute_command(command):
    var_result = subprocess.call(command, shell=True)
    if var_result != 0:
        raise Exception, "Run command '" + command + "' failed"