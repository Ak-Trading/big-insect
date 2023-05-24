import subprocess

subprocess.run(["docker", "run", "-p", "80:80", "--rm", "webhook"])
