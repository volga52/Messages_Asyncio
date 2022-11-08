import subprocess

# command to be executed
command = "pip install pymysql"

# system command
res = subprocess.check_output(command)

# type of the value returned
print("Return type: ", type(res))

# decoded result
print("Decoded string: ", res.decode("utf-8"))
