import os
import pytest
from python_on_whales.client_config import ClientConfig
from python_on_whales.docker_client import DockerClient
import shutil

@pytest.fixture
def docker():
    config = ClientConfig(
        client_binary_path=os.environ.get("CONTAINER_RUNTIME", shutil.which("docker"))
    )
    yield DockerClient(client_config=config)
