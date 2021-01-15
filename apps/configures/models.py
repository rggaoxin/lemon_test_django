from django.db import models

from utils.base_models import BaseModel


class Configures(BaseModel):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField('配置名称', max_length=50, help_text='配置名称')
    interface = models.ForeignKey('interfaces.Interfaces',
                                  on_delete=models.CASCADE,
                                  related_name='configures',
                                  help_text='所属接口')
    author = models.CharField('编写人员', max_length=50, help_text='编写人员')
    request = models.TextField('请求信息', help_text='请求信息')

    class Meta:
        db_table = 'tb_configures'
        verbose_name = '配置信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
