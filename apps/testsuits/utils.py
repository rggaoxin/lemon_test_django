from testcases.models import Testcases


def modify_output(datas):
    datas_list = []
    for item in datas:
        # create_time格式化
        create_time_list = item.get('create_time').split('T')
        first_part = create_time_list[0]
        second_part = create_time_list[1].split('.')[0]
        item['create_time'] = first_part + ' ' + second_part

        # update_time 进行格式化
        update_time_list = item.get('update_time').split('T')
        first_part = update_time_list[0]
        second_part = update_time_list[1].split('.')[0]
        item['update_time'] = first_part + ' ' + second_part

        datas_list.append(item)
    return datas_list


def get_testcases_by_interface_ids(ids_list):
    """
    通过接口id获取用例
    :param ids_list:
    :return:
    """
    one_list = []
    for interface_id in ids_list:
        # 返回一个查询集, 查询集中的每一个元素为用例id值
        # [1, 2, 3]
        testcases_qs = Testcases.objects.values_list('id', flat=True).\
            filter(interface_id=interface_id)
        one_list.extend(list(testcases_qs))
    return one_list
