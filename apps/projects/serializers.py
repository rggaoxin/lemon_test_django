from rest_framework import serializers

from debugtalks.models import DebugTalks
from testcases.models import Testcases
from utils import validates
from .models import Projects


class ProjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        exclude = ('update_time', 'is_delete')

        extra_kwargs = {
            'create_time': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        project_obj = super().create(validated_data)
        DebugTalks.objects.create(project=project_obj)

        return project_obj


class ProjectNamesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name')


class ProjectsRunSerializer(serializers.ModelSerializer):
    """
    运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量ID',
                                      validators=[validates.whether_existed_env_id])

    class Meta:
        model = Testcases
        fields = ('id', 'env_id')
