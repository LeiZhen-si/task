import json
import time
import os
import requests
import zipfile

base_url = 'http://127.0.0.1:5001'
upload_url = base_url +'/upload'
report_list_url = base_url +'/report/list'
base_sync_dir = '/home/sssbjlx205/Documents/workspace/Node-red/validation-tool/task/flask-vue-crud/client'
sync_report_folder = base_sync_dir + '/tasks'  # 当前文件夹


def get_server_dir_list():
    response = requests.get(report_list_url)
    # print(type(response.text))
    # print(type(json.loads(response.text)))
    jsonobj = json.loads(response.text)
    print(jsonobj['data'])
    # print(type(jsonobj['data']))
    # for key in jsonobj:
    #     print(key)
    #     print(jsonobj[key])
    return jsonobj['data']

def get_local_dir_list():
    folder = sync_report_folder
    # print(folder)

    # 获取文件夹下所有文件和文件夹
    files = os.listdir(folder)

    # 遍历并判断是否为文件夹
    folders = []
    for file in files:
        full_path = os.path.join(folder, file)
        if os.path.isdir(full_path):
            folders.append(file)

    print(folders)
    return folders

def compare_dir():
    # 获取当前全部文件 和 文件夹
    local_dirs = get_local_dir_list()
    server_dir = get_server_dir_list()

    # 计算新增文件 和 文件夹
    new_dirs = set(local_dirs).difference(set(server_dir))
    print(new_dirs)

    # 如果有新增,压缩，上传
    if new_dirs:
        for dir_name in new_dirs:
            print(dir_name)
            # 压缩文件夹
            zip_name = dir_name + '.zip'
            file_path = sync_report_folder + '/' + dir_name
            zip_file_path = sync_report_folder + '/'+zip_name
            print(zip_file_path)
            print(file_path)
            print("--------------compress start----------------")
            zip_folder(file_path, zip_file_path)
            print("--------------compress finish , uploading----------------")
            # # 上传服务器
            upload_zip_file(zip_file_path,zip_name)


def writeZip(zf, file, arc_path=None):
    """迭代压缩文件夹"""
    # 设置压缩路径
    if arc_path is None:
        arc_path = rf'\{os.path.basename(file)}'

    # 先压缩本文件
    zf.write(file, arc_path)

    # 如果是文件夹
    if os.path.isdir(file):
        # 获取它所有的子文件
        inner_files = os.listdir(file)
        # 将所有的子文件压缩
        for inner_file in inner_files:
            inner_file = f'{file}{os.sep}{inner_file}'
            arc = fr'{arc_path}\{os.path.basename(inner_file)}'
            writeZip(zf, inner_file, arc)


def zip_folder(dir_path, zip_full_name):
    """
    压缩文件夹下所有子文件夹和文件
    :param dirpath: 目标文件夹路径
    :param zip_full_name: zip文件绝对路径
    """
    dirpath = dir_path
    with zipfile.ZipFile(zip_full_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for dir_full_path, dir_names, file_names in os.walk(dir_path):
            # zip压缩包内的相对路径
            dir_path_inzip = dir_full_path.replace(dirpath, '')
            for dir_name in dir_names:
                zf.write(os.path.join(dir_full_path, dir_name), os.path.join(dir_path_inzip, dir_name))
            for file_name in file_names:
                zf.write(os.path.join(dir_full_path, file_name), os.path.join(dir_path_inzip, file_name))
    zf.close()


def upload_zip_file(zip_file,file_name):
    url = 'http://localhost:5001/upload'

    # 选择 zip 文件
    # zip_file = 'path/to/file.zip'
    print(zip_file)
    # 读取二进制数据
    with open(zip_file, 'rb') as f:
        data = f.read()

    # 定义文件字段
    files = {
        'the_zip_file': (file_name, data)
    }

    # 发起请求,上传 zip 文件
    response = requests.post(url, files=files)
    print(response.text)


if __name__ == '__main__':
    import datetime
    while True:
        print("start compare sync dir : {}".format( datetime.datetime.now()))
        compare_dir()
        time.sleep(60)

    #  对比文件夹
    # get_server_dir_list()
    # get_local_dir_list()
    # compare_dir()

    # # 压缩文件夹
    # file_path = '/home/sssbjlx205/Documents/workspace/Node-red/validation-tool/task/flask-vue-crud/client/tasks/test3'
    # zip_file_path = file_path + '.zip'
    # print(zip_file_path)
    #
    # zip_folder(file_path,zip_file_path)
    #
    # # 上传服务器
    # upload_zip_file(zip_file_path)

