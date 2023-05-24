import subprocess

subprocess.run(["docker", "build", "-t", "webhook", "."])

subprocess.run(["docker", "run", "-p", "80:80", "--rm", "webhook"])
