from django.db.models import Count

from interfaces.models import Interfaces
from testsuits.models import Testsuits


def get_count_by_project(datas):
    """
    1. 通过项目中的接口、用例、配置、套件的数量
    2. 对时间进行格式化
    :param datas:
    :return:
    """
    datas_list = []
    for item in datas:
        # create_time格式化
        create_time_list = item.get('create_time').split('T')
        first_part = create_time_list[0]
        second_part = create_time_list[1].split('.')[0]
        item['create_time'] = first_part + ' ' + second_part

        # 获取项目id值
        project_id = item['id']
        interfaces_testcases_objs = Interfaces.objects.values('id').annotate(testcases=Count('testcases')).\
            filter(project_id=project_id)
        # 获取接口总数
        interfaces_count = interfaces_testcases_objs.count()
        # 设置用例总数初始值为0
        testcases_count = 0
        for one_dict in interfaces_testcases_objs:
            testcases_count += one_dict['testcases']

        interfaces_configures_objs = Interfaces.objects.values('id').annotate(configures=Count('configures')). \
            filter(project_id=project_id)

        # 设置配置总数初始值为0
        configures_count = 0
        for one_dict in interfaces_configures_objs:
            configures_count += one_dict['configures']

        # 获取套件总数
        testsuits_count = Testsuits.objects.filter(project_id=project_id).count()

        item['interfaces'] = interfaces_count
        item['testsuits'] = testsuits_count
        item['testcases'] = testcases_count
        item['configures'] = configures_count

        datas_list.append(item)
    return datas_list
