import time
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import subprocess
from threading import Thread
import os
def get_task_report(task_name):
    report_list = all_report()
    print(type(report_list))
    print("------------end--------------------------")
    # for report in report_list:
    #     if report.get('task_name') == 'test':
    #         print(report)

def all_report():
    folder = '/home/sssbjlx205/Documents/workspace/Node-red/validation-tool/task-dashboard/task/backend/sync_folder/tasks'
    print("\n-------------files end-------------------------\n")
    print("sync folder tasks : {}".format(folder))
    json_obj = {}
    task_list = []
    level_type = 'folder' # folder or file ,
    for root, dirs, files in os.walk(folder):
        level = root.replace(folder, '').count(os.sep)
        print(" level : {}".format(level))
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        # print(os.path.abspath(root))  # 打印文件夹路径
        report_type = ''
        # 一级目录 和 二级目录
        if level == 1:  # 一级目录是task_name
            if json_obj != {}:
                task_list.append(json_obj)
                json_obj = {}
                print("\n-------------files end-------------------------\n")

            json_obj.setdefault("task_name", os.path.basename(root))
            json_obj.setdefault("abs_path", os.path.abspath(root))
        elif level == 2:  # 二级目录是report分类，cdt/power/temperature
            report_type = os.path.basename(root)

        subindent = ' ' * 4 * (level + 1)
        report_files = []
        for f in files:
            print('files : {}{}'.format(subindent, f))
            print(os.path.abspath(os.path.join(root, f)))
            report_files.append(f)

        if report_type != '' and report_files.__len__() > 0:
            json_obj.setdefault(report_type, report_files)

    # 最后一组
    task_list.append(json_obj)
    json_obj = {}
    print(task_list)
    print("\n----------------all_report-----end-----------------\n")

    return task_list

def all_report_2():
    folder = '/home/sssbjlx205/Documents/workspace/Node-red/validation-tool/task-dashboard/task/backend/sync_folder/tasks'
    print("\n-------------files end-------------------------\n")
    print("sync folder tasks : {}".format(folder))
    json_obj = {}
    task_list = []
    current_path = []
    level_type = 'folder' # folder or file ,
    level = 0
    parent = []
    for root, dirs, files in os.walk(folder):
        print("-----------------level start---------------------------")
        print("root: {}".format(root))
        print("file_name:{}".format(os.path.basename(root)))
        print("dirs: {}".format(dirs))
        print("files: {}".format(files))
        print(os.pardir)
        current_obj = {}
        current_path_all = []

        for dir in dirs:
            current_path_all.append(dir)

        for file in files:
            current_path_all.append(file)

        # current_obj.setdefault(os.path.basename(root),current_path_all)

        if parent == []:
            parent = current_path_all
        else:
            for par in parent :
                if par == os.path.basename(root):
                    parent.append(par, current_path_all)
                    break
        # print()
        print("-----------------level end---------------------------")

    print(task_list)

def all_report_name():
    folder = './server/tasks'
    print(folder)

    # 获取文件夹下所有文件和文件夹
    files = os.listdir(folder)

    # 遍历并判断是否为文件夹
    folders = []
    for file in files:
        full_path = os.path.join(folder, file)
        if os.path.isdir(full_path):
            folders.append(file)

    print(folders)

    print("\n----------------all_report-----end-----------------\n")

if __name__ == '__main__':
    all_report_2()
    # all_report_name()
    # name = 'test.zip'
    # print(name[:-4])
    # get_task_report("tsk")
    # import config.settings
    #
    # url = config.settings.APP_ENV.URL
    # token = config.settings.APP_ENV.TOKEN
    # org = config.settings.APP_ENV.ORG
    # # Create InfluxDB client object
    # client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
    # query = 'from(bucket: "sdc_task_01") |> data'
    # tables = client.query_api().query(query=query,org=org)
    # # tables = client.get_list_measurements()
    # # tables = client.query_api().query(query, org=org)
    #
    # print(tables.to_json())

    #-------------------------------------------------------------------
    # files = {}
    # exist_files = {}
    # import os
    #
    # folder = './server/tasks'
    # print(folder)
    # json_obj = {}
    # task_list = []
    # for root, dirs, files in os.walk(folder):
    #     level = root.replace(folder, '').count(os.sep)
    #     print(" level : {}".format( level))
    #     indent = ' ' * 4 * (level)
    #     print('{}{}/'.format(indent, os.path.basename(root)))
    #     # print(os.path.abspath(root))  # 打印文件夹路径
    #     report_type = ''
    #     if level == 1: # 一级目录是task_name
    #         if json_obj != {} :
    #             task_list.append(json_obj)
    #             json_obj = {}
    #             print("\n-------------files end-------------------------\n")
    #
    #         json_obj.setdefault("task_name",os.path.basename(root))
    #         json_obj.setdefault("abs_path", os.path.abspath(root))
    #     elif level == 2 : # 二级目录是report分类，cdt/power/temperature
    #         report_type = os.path.basename(root)
    #
    #     subindent = ' ' * 4 * (level + 1)
    #     report_files = []
    #     for f in files:
    #         print('files : {}{}'.format(subindent, f))
    #         print(os.path.abspath(os.path.join(root, f)))
    #         report_files.append(f)
    #
    #     if report_type != '' and report_files.__len__() > 0:
    #         json_obj.setdefault(report_type,report_files)
    #
    # # 最后一组
    # task_list.append(json_obj)
    # json_obj = {}
    #
    # print("\n--------------------------------------\n")
    # print(task_list)
