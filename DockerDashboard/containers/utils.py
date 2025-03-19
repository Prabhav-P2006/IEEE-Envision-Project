import docker

def get_docker_client():
    try:
        client = docker.from_env()
        return client
    except docker.errors.DockerException as e:
        print(f"Error connecting to Docker: {e}")
        return None

def get_all_containers():
    client = get_docker_client()
    if client:
        return client.containers.list(all=True)
    return []