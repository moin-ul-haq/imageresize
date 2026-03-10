from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    image=serializers.ImageField()


class TaskStatusSerializer(serializers.Serializer):
    task_id=serializers.IntegerField()