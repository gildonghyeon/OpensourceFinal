import subprocess

def run_cmd():
    cmd_output = subprocess.check_output(["dir"], shell=True, stderr=subprocess.STDOUT)
    return cmd_output.decode("utf-8")
