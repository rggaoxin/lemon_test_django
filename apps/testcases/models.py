from django.db import models

from utils.base_models import BaseModel


class Testcases(BaseModel):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField('用例名称', max_length=50, unique=True, help_text='用例名称')
    interface = models.ForeignKey('interfaces.Interfaces', on_delete=models.CASCADE,
                                  help_text='所属接口')
    # include = models.ForeignKey('', on_delete=models.SET_NULL, null=True, related_name='testcases')
    include = models.TextField('前置', null=True, help_text='用例执行前置顺序')
    author = models.CharField('编写人员', max_length=50, help_text='编写人员')
    request = models.TextField('请求信息', help_text='请求信息')

    class Meta:
        db_table = 'tb_testcases'
        verbose_name = '用例信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
