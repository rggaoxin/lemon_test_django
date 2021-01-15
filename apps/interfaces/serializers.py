from rest_framework import serializers

from .models import Interfaces
from projects.models import Projects
from utils import validates


class InterfacesSerializer(serializers.ModelSerializer):
    # read_only = True
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(),
                                                    label='项目id', help_text='项目id')


    class Meta:
        model = Interfaces
        fields = ('id', 'name', 'tester', 'create_time', 'desc', 'project', 'project_id')

    def create(self, validated_data):
        project = validated_data.pop('project_id')
        validated_data['project'] = project
        # Interfaces.objects.create(project_id=1)
        # Interfaces.objects.create(project=某个项目对象)
        interface = Interfaces.objects.create(**validated_data)
        return interface

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project

        return super().update(instance, validated_data)


class InterfaceRunSerializer(serializers.ModelSerializer):
    """
    通过接口来运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量ID',
                                      validators=[validates.whether_existed_env_id])

    class Meta:
        model = Interfaces
        fields = ('id', 'env_id')
