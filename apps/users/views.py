from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers


class RegisterView(CreateAPIView):
    """
    注册接口
    """
    serializer_class = serializers.RegisterSerializer
    # 如果某个视图中, 没有获取信息的接口, 那么可以不用指定queryset类属性


class UsernameValidateView(APIView):
    """
    校验用户名
    """

    def get(self, request, username):
        data_dict = {
            "username": username,
            "count": User.objects.filter(username=username).count()
        }
        return Response(data_dict)


class EmailValidateView(APIView):
    """
    校验邮箱
    """

    def get(self, request, email):
        data_dict = {
            "email": email,
            "count": User.objects.filter(email=email).count()
        }
        return Response(data_dict)
