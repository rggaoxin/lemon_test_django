def get_file_content(filename):
    """
    读取文件, 返回一个生成器对象
    :param filename:
    :return:
    """
    with open(filename, encoding='utf-8') as f:
        while True:
            line = f.read(512)
            if line:
                yield line
            else:  # 如果line为None, 那么说明已经读取到文件末尾
                break


def format_output(datas):
    datas_list = []
    for item in datas:
        result = 'Pass' if item['result'] else 'Fail'

        # create_time格式化
        create_time_list = item.get('create_time').split('T')
        first_part = create_time_list[0]
        second_part = create_time_list[1].split('.')[0]

        item['create_time'] = first_part + ' ' + second_part
        item['result'] = result
        datas_list.append(item)
    return datas_list
