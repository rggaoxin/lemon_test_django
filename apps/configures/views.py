import json

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from interfaces.models import Interfaces
from utils import handle_datas
from .models import Configures
from .serializers import ConfiguresSerializer


class ConfiguresViewSet(ModelViewSet):
    """
    list:
    返回配置信息（多个）列表数据

    create:
    创建配置信息

    retrieve:
    返回配置信息（单个）详情数据

    update:
    更新（全）配置信息

    partial_update:
    更新（部分）配置信息

    destroy:
    删除配置信息

    retrieve:
    获取配置详情
    """
    queryset = Configures.objects.all()
    serializer_class = ConfiguresSerializer
    permission_classes = (permissions.IsAuthenticated, )
    ordering_fields = ('id', 'name')

    def retrieve(self, request, *args, **kwargs):
        config_obj = self.get_object()
        config_request = json.loads(config_obj.request, encoding='utf-8')

        # 处理请求头数据
        config_headers = config_request['config']['request'].get('headers')
        config_headers_list = handle_datas.handle_data4(config_headers)

        # 处理全局变量数据
        config_variables = config_request['config'].get('variables')
        config_variables_list = handle_datas.handle_data2(config_variables)

        config_name = config_request['config']['name']
        selected_interface_id = config_obj.interface_id
        selected_project_id = Interfaces.objects.get(id=selected_interface_id).project_id

        datas = {
            "author": config_obj.author,
            "configure_name": config_name,
            "selected_interface_id": selected_interface_id,
            "selected_project_id": selected_project_id,
            "header": config_headers_list,
            "globalVar": config_variables_list
        }

        return Response(datas)
