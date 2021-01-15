from rest_framework import serializers

from .models import Reports


class ReportsSerializer(serializers.ModelSerializer):
    """
    报告序列化器类
    """

    class Meta:
        model = Reports
        exclude = ('update_time', )

        extra_kwargs = {
            'create_time': {
                'read_only': True
            },

        }
