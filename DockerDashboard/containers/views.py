from django.shortcuts import render, redirect
from .utils import get_all_containers, get_docker_client

def container_list(request):
    containers = get_all_containers()
    return render(request, 'containers/container_list.html', {'containers': containers})

def container_action(request, container_id, action):
    client = get_docker_client()
    if not client:
        return redirect('container_list')
    
    container = client.containers.get(container_id)
    if action == 'start':
        container.start()
    elif action == 'stop':
        container.stop()
    elif action == 'restart':
        container.restart()
    
    return redirect('container_list')

def container_logs(request, container_id):
    client = get_docker_client()
    try:
        container = client.containers.get(container_id)
        logs = container.logs(
            stdout=True,
            stderr=True,
            timestamps=False,
            tail=100  # Show last 100 lines (adjust as needed)
        ).decode('utf-8', errors='replace')
        print(f"Logs for {container_id}: {logs[:200]}...")  # Print first 200 chars  # Handle non-UTF-8 characters
    except docker.errors.NotFound:
        logs = f"Container {container_id} not found!"
    except docker.errors.APIError as e:
        logs = f"Error fetching logs: {str(e)}"
    except Exception as e:
        logs = f"Unexpected error: {str(e)}"
    
    return render(request, 'containers/logs.html', {'logs': logs})