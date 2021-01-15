import logging
import os
from datetime import datetime

from django.conf import settings
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from envs.models import Envs
from interfaces.models import Interfaces
from testcases.models import Testcases
from utils import common
from . import serializers
from .models import Projects
from .utils import get_count_by_project

logger = logging.getLogger("test")


class ProjectViewSet(viewsets.ModelViewSet):
    """
    create:
    创建项目

    retrieve:
    获取项目详情数据

    update:
    完整更新项目

    partial_update:
    部分更新项目

    list:
    获取项目列表数据

    destroy:
    删除项目

    names:
    获取所有的项目名和项目ID

    interfaces:
    获取某个项目下的所有接口信息

    """
    queryset = Projects.objects.all()
    serializer_class = serializers.ProjectModelSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_fields = ['name', 'leader', 'tester']
    ordering_fields = ['id', 'name', 'leader']
    permission_classes = [permissions.IsAuthenticated]

    # 在实际项目中, 如何创建接口呢?
    # 1. 优先使用框架提供的功能
    # 2. 如果框架提供的功能不满足需要
    # a. 如果只有少量的地方不满足, 可以拓展父类提供的方法
    # b. 如果绝大多数的地方都不满足, 就自己实现
    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        #
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     # datas = get_count_by_project(serializer.data)
        #     return self.get_paginated_response(datas)
        #
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
        # print(1/0)
        response = super().list(request, *args, **kwargs)
        response.data['results'] = get_count_by_project(response.data['results'])
        return response

    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def interfaces(self, request, pk=None):
        interface_obj = Interfaces.objects.filter(project_id=pk)
        one_list = []
        for obj in interface_obj:
            one_list.append({
                "id": obj.id,
                "name": obj.name
            })
        return Response(data=one_list)

    @action(methods=['post'], detail=True)
    def run(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        datas = serializer.validated_data
        env_id = datas.get('env_id')  # 获取环境变量env_id
        env = Envs.objects.get(id=env_id)

        # 创建测试用例所在目录名
        testcase_dir_path = os.path.join(settings.SUITES_DIR,
                                         datetime.strftime(datetime.now(), "%Y%m%d%H%M%S%f"))
        if not os.path.exists(testcase_dir_path):
            os.mkdir(testcase_dir_path)

        interface_objs = Interfaces.objects.filter(project=instance)
        if not interface_objs.exists():  # 如果此项目下没有接口, 则无法运行
            data_dict = {
                "detail": "此项目下无接口, 无法运行!"
            }
            return Response(data_dict, status=status.HTTP_400_BAD_REQUEST)

        for inter_obj in interface_objs:
            testcase_objs = Testcases.objects.filter(interface=inter_obj)

            for one_obj in testcase_objs:
                common.generate_testcase_files(one_obj, env, testcase_dir_path)  # 传入接口对象，环境 ，用例目录

        # 运行用例
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        """
        不同的action选择不同的序列化器
        :return:
        """
        if self.action == 'names':
            return serializers.ProjectNamesModelSerializer
        elif self.action == 'run':
            return serializers.ProjectsRunSerializer
        else:
            return self.serializer_class
