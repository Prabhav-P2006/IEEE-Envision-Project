from django.shortcuts import render, redirect
from .utils import get_all_containers, get_docker_client
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import docker
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, 'Registration successful! Welcome to Docker Dashboard.')
            return redirect('container_list')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully')
    return render(request, 'registration/logout.html')

@login_required
def container_list(request):
    containers = get_all_containers()
    return render(request, 'containers/container_list.html', {'containers': containers})

@login_required
def container_action(request, container_id, action):
    client = get_docker_client()
    if not client:
        messages.error(request, 'Failed to connect to Docker')
        return redirect('container_list')
    
    try:
        container = client.containers.get(container_id)
        if action == 'start':
            container.start()
            messages.success(request, f'Container {container.name} started successfully')
        elif action == 'stop':
            container.stop()
            messages.success(request, f'Container {container.name} stopped successfully')
        elif action == 'restart':
            container.restart()
            messages.success(request, f'Container {container.name} restarted successfully')
    except docker.errors.APIError as e:
        messages.error(request, f'Error performing action: {str(e)}')
    
    return redirect('container_list')

@login_required
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
    except docker.errors.NotFound:
        logs = f"Container {container_id} not found!"
        messages.error(request, 'Container not found')
    except docker.errors.APIError as e:
        logs = f"Error fetching logs: {str(e)}"
        messages.error(request, f'Error fetching logs: {str(e)}')
    except Exception as e:
        logs = f"Unexpected error: {str(e)}"
        messages.error(request, f'Unexpected error: {str(e)}')
    
    return render(request, 'containers/logs.html', {'logs': logs})