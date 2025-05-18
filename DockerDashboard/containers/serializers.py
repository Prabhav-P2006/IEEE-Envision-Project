from rest_framework import serializers

class ContainerSerializer(serializers.Serializer):
    id = serializers.CharField(source='short_id')
    name = serializers.CharField()
    status = serializers.CharField()
    image = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    def get_image(self, obj):
        try:
            return obj.image.tags[0] if obj.image.tags else "untagged"
        except:
            return "unknown"

    def get_created(self, obj):
        try:
            return obj.attrs['Created']
        except (KeyError, AttributeError):
            return None