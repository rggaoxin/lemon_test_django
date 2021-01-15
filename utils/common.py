import json
import logging
import os
from datetime import datetime

import yaml
from httprunner.exceptions import ParamsError
from httprunner.task import HttpRunner
from rest_framework import status
from rest_framework.response import Response

from configures.models import Configures
from debugtalks.models import DebugTalks
from reports.models import Reports
from testcases.models import Testcases

logger = logging.getLogger('test')


def timestamp_to_datetime(summary, type=True):
    if not type:
        time_stamp = int(summary["time"]["start_at"])
        summary['time']['start_datetime'] = datetime. \
            fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

    for detail in summary['details']:
        try:
            time_stamp = int(detail['time']['start_at'])
            detail['time']['start_at'] = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass

        for record in detail['records']:
            try:
                time_stamp = int(record['meta_data']['request']['start_timestamp'])
                record['meta_data']['request']['start_timestamp'] = \
                    datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                pass
    return summary


def generate_testcase_files(instance, env, testcase_dir_path):
    testcases_list = []
    config = {
        'config': {
            'name': instance.name,
            'request': {
                'base_url': env.base_url if env else ''
            }
        }
    }
    testcases_list.append(config)

    # include = eval(instance.include)
    # request = eval(instance.request)
    # 获取当前用例的前置配置和前置用例
    include = json.loads(instance.include, encoding='utf-8')
    # 获取当前用例的请求信息
    request = json.loads(instance.request, encoding='utf-8')

    interface_name = instance.interface.name  # 接口名称
    project_name = instance.interface.project.name  # 项目名称

    testcase_dir_path = os.path.join(testcase_dir_path, project_name)
    # 创建项目名所在文件夹
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
        debugtalk_obj = DebugTalks.objects.filter(project__name=project_name).first()
        if debugtalk_obj:
            debugtalk = debugtalk_obj.debugtalk
        else:
            debugtalk = ""

        # 创建debugtalk.py文件
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'),
                  mode='w',
                  encoding='utf-8') as one_file:
            one_file.write(debugtalk)

    testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
    # 在项目目录下创建接口名所在文件夹
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    # {'config': 2, 'testcases': [2,5]}
    # 如果include前置中有config, 那么添加到testcases_list中
    if 'config' in include:
        config_id = include.get('config')
        config_obj = Configures.objects.filter(id=config_id).first()
        if config_obj:
            # 需要将请求头(当前为嵌套字典的列表), 需要转化为字典
            # config_request = eval(config_obj.request)
            config_request = json.loads(config_obj.request, encoding='utf-8')

            # config_request = eval(config_obj.request)
            # config_request.get('config').get('request').setdefault('base_url', env.base_url)
            # config_dict = config_request.get('config')
            # config_dict['request']['base_url'] = env.base_url
            # config_request['config']['name'] = instance.name
            config_request['config']['request']['base_url'] = env.base_url  # 添加公共配置的公共url
            # testcases_list.append(config_request)
            testcases_list[0] = config_request

    # 如果include前置中有testcases, 那么添加到testcases_list中
    if 'testcases' in include:
        for t_id in include.get('testcases'):
            testcase_obj = Testcases.objects.filter(id=t_id).first()
            if testcase_obj:
                try:
                    # testcase_request = eval(testcase_obj.request)
                    testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
                except Exception as e:
                    logger.error(e)
                    continue
                else:
                    testcases_list.append(testcase_request)

    # 将当前用例的request添加到testcases_list
    testcases_list.append(request)

    with open(os.path.join(testcase_dir_path, instance.name + '.yml'),
              mode="w", encoding="utf-8") as one_file:
        yaml.dump(testcases_list, one_file, allow_unicode=True)


def create_report(runner, report_name=None):
    """
    创建测试报告
    :param runner:
    :param report_name:
    :return:
    """
    time_stamp = int(runner.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime
    # duration保留3位小数
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    for item in runner.summary['details']:
        try:
            for record in item['records']:
                record['meta_data']['response']['content'] = record['meta_data']['response']['content']. \
                    decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request'].get('body')
                if request_body is None:
                    continue
                if isinstance(request_body, bytes):
                    record['meta_data']['request']['body'] = request_body.decode('utf-8', errors='ignore')
                if "files" in record['meta_data']['request'].keys():
                    record['meta_data']['request'].pop("files")
                    if "body" in record['meta_data']['request'].keys():
                        record['meta_data']['request'].pop("body")
        except Exception as e:
            continue

    summary = json.dumps(runner.summary, ensure_ascii=False)

    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    report_path = runner.gen_html_report(html_report_name=report_name)

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),
        'count': runner.summary.get('stat').get('testsRun'),
        'html': reports,
        'summary': summary
    }
    report_obj = Reports.objects.create(**test_report)
    return report_obj.id


def run_testcase(instance, testcase_dir_path):
    """
    运行用例
    :return:
    :param instance: 实例
    :param testcase_dir_path: 用例根目录路径
    :return dict
    """
    runner = HttpRunner()
    # runner.run(testcase_dir_path)
    try:
        runner.run(testcase_dir_path)
    except ParamsError:
        logger.error("用例参数有误")
        data = {
            "msg": "用例参数有误"
        }
        return Response(data, status=400)

    runner.summary = timestamp_to_datetime(runner.summary, type=False)

    try:
        report_name = instance.name
    except Exception as e:
        report_name = '被遗弃的报告' + '-' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')

    report_id = create_report(runner, report_name=report_name)
    data_dict = {
        "id": report_id
    }

    return Response(data_dict, status=status.HTTP_201_CREATED)
