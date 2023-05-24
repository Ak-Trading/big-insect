from docker import DockerClient
import subprocess


client = DockerClient()

images = client.images.list()

for image in images:
    if image.attrs["RepoTags"][0].split(":")[0] == "webhook":
        image.remove()

subprocess.run(["docker", "build", "-t", "webhook", "."])

subprocess.run(["docker", "run", "-p", "80:80", "--rm", "webhook"])
