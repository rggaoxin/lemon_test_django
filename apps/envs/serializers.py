from rest_framework import serializers

from .models import Envs


class EnvsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Envs
        fields = ('id', 'name', 'base_url', 'create_time', 'desc')


class EnvNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envs
        fields = ('id', 'name')
