from django.db import models

from utils.base_models import BaseModel


class Envs(BaseModel):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField(verbose_name='环境名称', max_length=200, unique=True, help_text='环境名称')
    base_url = models.URLField(verbose_name='请求base url', max_length=200, help_text='请求base url')
    desc = models.CharField(verbose_name='简要描述', max_length=200, help_text='简要描述')

    class Meta:
        db_table = 'tb_envs'
        verbose_name = '环境信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
