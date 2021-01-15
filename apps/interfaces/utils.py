from configures.models import Configures
from testcases.models import Testcases


def get_count_by_interface(datas):
    datas_list = []
    for item in datas:
        interface_id = item['id']
        # 计算用例数
        testcases_count = Testcases.objects.filter(interface_id=interface_id).count()

        # 计算配置数
        config_count = Configures.objects.filter(interface_id=interface_id).count()
        create_time = datas[0]['create_time']
        item['create_time'] = create_time.split('T')[0] + ' ' + create_time.split('T')[1].split('.')[0]
        item['testcases'] = testcases_count
        item['configures'] = config_count
        datas_list.append(item)
    return datas_list
