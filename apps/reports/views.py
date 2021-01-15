import os
import json

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.http import StreamingHttpResponse
from django.utils.encoding import escape_uri_path

from .models import Reports
from .serializers import ReportsSerializer
from .utils import get_file_content, format_output


class ReportsViewSet(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    """
    """
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    ordering_fields = ('id', 'name')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['results'] = format_output(response.data['results'])

        return response

    @action(detail=True)
    def download(self, *args, **kwargs):
        # 1. 手动创建报告
        instance = self.get_object()
        html = instance.html

        report_path = settings.REPORTS_DIR
        report_full_path = os.path.join(report_path, instance.name) + '.html'
        with open(report_full_path, 'w', encoding='utf-8') as file:
            file.write(html)

        # 2. 读取创建的报告并返回给前端
        # 如果要提供前端用户能够下载文件, 那么需要在响应头中添加如下字段:
        # Content-Type = application/octet-stream
        # Content-Disposition = attachment; filename*=UTF-8'' 文件名
        response = StreamingHttpResponse(get_file_content(report_full_path))
        # 对文件名进行转义
        report_path_final = escape_uri_path(instance.name + '.html')
        # StreamingHttpResponse对象类似于dict字典
        # 如果以字典的形式添加key-value, 那么添加的是响应头信息
        response['Content-Type'] = 'application/octet-stream'
        # response['Content-Disposition'] = "attachment;filename*=UTF-8''{}".format(report_path_final)
        # response['Content-Disposition'] = "attachment;filename={}".format(report_path_final)
        response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(report_path_final)

        return response

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        datas = serializer.data
        try:
            datas['summary'] = json.loads(datas['summary'], encoding='utf-8')
        except Exception as e:
            pass
        return Response(datas)
