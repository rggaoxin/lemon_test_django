from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Envs
from .serializers import EnvsSerializer, EnvNameSerializer
from .utils import handle_env


class EnvsViewSet(ModelViewSet):
    """
    list:
    返回环境变量（多个）列表数据

    create:
    创建环境变量

    retrieve:
    返回环境变量（单个）详情数据

    update:
    更新（全）环境变量

    partial_update:
    更新（部分）环境变量

    destroy:
    删除环境变量

    names:
    返回所有环境变量ID和名称
    """
    queryset = Envs.objects.all()
    serializer_class = EnvsSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ('id', 'name')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['results'] = handle_env(response.data['results'])

        return response

    @action(methods=['get'], detail=False)
    def names(self, request, pk=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'names':
            return EnvNameSerializer
        else:
            return EnvsSerializer
