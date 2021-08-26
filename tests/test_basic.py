"""Test basic access to docker/podman."""
from python_on_whales.docker_client import DockerClient

def test_basic(docker: DockerClient):
    print(docker.run("hello-world", remove=True))
    assert False
