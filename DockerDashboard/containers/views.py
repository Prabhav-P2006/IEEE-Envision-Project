from django.shortcuts import render, redirect
from .utils import get_all_containers, get_docker_client
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import docker
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContainerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

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
@api_view(['GET'])
def container_list(request):
    containers = get_all_containers()
    if request.accepts('text/html'):
        return render(request, 'containers/container_list.html', {'containers': containers})

    serializer = ContainerSerializer(containers, many = True)
    return Response({
        'count': len(containers), 
        'results': serializer.data 
        })


@login_required
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def container_action(request, container_id, action):
    client = get_docker_client()
    if not client:
        if request.accepts('text/html'):
            messages.error(request, 'Failed to connect to Docker')
            return redirect('container_list')
        return Response({'error': 'Dcoker connection failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    try:
        container = client.containers.get(container_id)
        action_methods = {
            'start': container.start,
            'stop': container.stop,
            'restart': container.restart,
            'pause': container.pause,
            'unpause': container.unpause,
            'delete': container.remove
        }
        
        if action in action_methods:
            action_methods[action]()
            msg = f'Container {container.name} {action}ed successfully'
            
            if request.accepts('text/html'):
                messages.success(request, msg)
                return redirect('container_list')
            return Response({'status': 'success', 'message': msg})
            
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    except docker.errors.APIError as e:
        error_msg = f'Error performing action: {str(e)}'
        if request.accepts('text/html'):
            messages.error(request, error_msg)
            return redirect('container_list')
        return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(['GET'])
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

