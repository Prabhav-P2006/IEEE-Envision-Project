from rest_framework import serializers

class ContainerSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    status = serializers.CharField()
    image = serializers.CharField()
    ports = serializers.ListField()
    created = serializers.DateTimeField()