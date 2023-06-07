import uuid
import datetime,time
from flask import Flask, jsonify, request, send_file,send_from_directory
from flask_cors import CORS
import config.settings
import json
import os
import zipfile
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# instantiate the app and connect  Influxdb
app = Flask(__name__)
app.config.from_object(__name__)


CORS(app, resources={r'/*': {'origins': '*'}})

url = config.settings.APP_ENV.URL
token = config.settings.APP_ENV.TOKEN
org = config.settings.APP_ENV.ORG
# Create InfluxDB client object
client = InfluxDBClient(url=url, token=token, org=org)

report_dir = config.settings.APP_ENV.BASETASKPATH

# 上传并解压
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['the_zip_file']
        print(f.filename)
        base_path = report_dir
        file_abs_path = base_path + '/' + f.filename
        f.save(file_abs_path)
        # 解压zip
        if zipfile.is_zipfile(file_abs_path):  # 判断是否zip文件
            zf = zipfile.ZipFile(file_abs_path, 'r')  # 设置文件为可读
            stem, suffix = os.path.splitext(f.filename)  # 提取文件名称
            for file in zf.namelist():  # 遍历文件
                zf.extract(file, base_path + "/" + stem)  # 解压至指定目录
    return 'Uploaded!!!!'


@app.route('/download/<report_name>', methods=['POST'])
def download(report_name):
    # file = report_dir + '/'+report_name + '/' + report_name + '.zip'
    file = report_dir + '/test.zip'
    print("report_naem: {}".format(file))
    file_size = os.path.getsize(file)
    print(file_size)
    response = send_file(file,
                         mimetype='application/zip',
                         attachment_filename=os.path.basename(file),
                         as_attachment=True)

    response.headers['Content-Length'] = file_size
    response.headers['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(file)
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Encoding'] = 'identity'
    print("response: {}".format(response))
    # return response
    return 'download!'


@app.route('/downloads/<path:path>', methods=['GET', 'POST'])
def downloads(path):
    '''
     根据指定路径提供下载服务
    '''
    # 指定可供下载的大目录
    print("--start downloads----: {}".format(path))
    root = report_dir

    root = root + '/' + path[:-4]
    # as_attachment参数设置为False，会展示预览，例如图片或pdf
    # send_from_directory(root, path, as_attachment=False)
    # return "download"
    return send_from_directory(root, path, as_attachment=False)


@app.route('/table/list', methods=['GET'])
def all_tables():
    tasks = all_task()
    # print(type(tasks))
    data = {
        'code': 20000,
        "data": tasks
    }
    return data

@app.route('/report/list', methods=['GET'])
def all_reports_dir():
    reports = all_report_name()
    # print(type(tasks))
    data = {
        'code': 20000,
        "data": reports
    }
    return data


@app.route('/table/detail/<task_id>', methods=['GET'])
def get_task_detail(task_id):
    # data = {'id': 'cf289978b41c453989c5cae59e314873', 'title': 'the Road', 'author': 'Jack Kerouac', 'read': True, 'task_name': 'tasssk-26', 'time': '1998-05-29T17:57:48.920000+00:00', 'start_time': '2023-05-29T17:51:28.270000+00:00', 'end_time': '2023-05-30T08:00:25.146642+00:00', 'description': 'validatin test task ', 'directory': 'task', 'type': 'Raspberry', 'version': '33'}
    print(task_id)
    data = get_task_by_id(int(task_id))
    print(data)
    result = {
        'code': 20000,
        'data': data
    }
    return result

def get_task_by_id(task_id):

    data = all_task()
    single_task = {}
    if data.__len__() > task_id:
        single_task = data[task_id]
        print(single_task.get('task_name'))
        # TODO  这个地方应该是根据task_name 获取report list
        report = get_task_report('test')
        single_task.setdefault('report',report)
    return single_task


@app.route('/tasks', methods=['GET'])
def all_task():
    # query = 'from(bucket: "sdc_task_01") |> range(start: -1h)'
    query = 'from(bucket: "sdc_task_01") |> range(start: 2023-05-20T17:51:28.270Z)'
    print(query)
    tables = client.query_api().query(query, org=org)

    # 将用户对象列表转换为JSON数组
    # print(tables.to_json())
    task_name = ""
    json_obj = {}
    task_list = []
    json_array = json.loads(tables.to_json())
    for table in json_array:
        # print(table["_start"])
        # print("measure : "+table['_measurement'])
        # print(type(table['_time']))
        # print(table['_field'])
        # print(table['_value'])
        if task_name == table['_measurement']:
            json_obj.setdefault(table['_field'], table['_value'])
            # print(json_obj)
        else :
            if task_name == "":
                task_name = table['_measurement']
                id = task_list.__len__()
                # ready to delete , start
                # json_obj.setdefault('id', uuid.uuid4().hex)
                # json_obj.setdefault('title', 'On the Road')
                # json_obj.setdefault('author','Jack Kerouac')
                # json_obj.setdefault('read',True)
                # ready to delete , end
                json_obj.setdefault("id", id)
                json_obj.setdefault("task_name", table['_measurement'])
                json_obj.setdefault("time", table['_time'])
                json_obj.setdefault("start_time", table['_start'])
                json_obj.setdefault("end_time", table['_stop'])
                json_obj.setdefault(table['_field'], table['_value'])
                # print("task_name : "+task_name)
                # print(json_obj)
            else:
                task_list.append(json_obj)
                task_name = ""
                json_obj = {}
                # print("task_list : " + task_list)
    if json_obj != {}:
        task_list.append(json_obj)
        task_name = ""
        json_obj = {}
    print(task_list)
    return task_list

def get_task_report(task_name):
    report_list = all_report()
    print(report_list)
    print("----------------get_task_report----------------------")
    for report in report_list:
        print(report)
        if report.get('task_name') == task_name:
            return report

def all_report_name():
    # folder = './server/tasks'
    folder = report_dir
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
    return folders

def all_report():
    folder = report_dir
    print(folder)
    json_obj = {}
    task_list = []
    for root, dirs, files in os.walk(folder):
        level = root.replace(folder, '').count(os.sep)
        print(" level : {}".format(level))
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        # print(os.path.abspath(root))  # 打印文件夹路径
        report_type = ''
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

    print("\n----------------all_report-----end-----------------\n")

    return task_list

# sdc_task_01
#  [{
#     start_time: start_time,
#     end_time: end_time,
#     type: hw_type,
#     version: dev_version,
#     directory: "task",
#     data: "validatin test task ",
#     time: new Date().getTime()
# },{
#     name: task_name
# }];
def add_task():
    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = Point("Task") \
        .tag("name", "task_name_01") \
        .field("start_time", "2023/05/26 22:52:47") \
        .field("end_time", "2023/05/26 23:52:47") \
        .field("type", "Nuttx") \
        .field("directory", "task") \
        .field("data", "validation test taks") \
        .time(datetime.utcnow(), WritePrecision.NS)

    write_api.write("sdc_task_01", org, point)

@app.route('/user/login', methods=['POST'])
def login():
    data = {
        'code': 20000,
        'data': "login success"
    }
    return data

from flask import make_response
#get方法:预览图片
@app.route('/show', methods=['GET'])
def show_photo():
    filename = request.values.get('filename')
    file_dir=os.path.join(os.getcwd()+'/sync_folder',filename)
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(file_dir, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass

#get方法:预览html
@app.route('/showhtml', methods=['GET'])
def show_html():
    filename = request.values.get('filename')
    file_dir=os.path.join(os.getcwd()+'/sync_folder',filename)
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(file_dir, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'text/html'
            return response
    else:
        pass

#get方法:视频，是默认下载了
@app.route('/showvideo', methods=['GET'])
def show_video():
    filename = request.values.get('filename')
    file_dir=os.path.join(os.getcwd()+'/sync_folder',filename)
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(file_dir, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'video/mpeg4'
            return response
    else:
        pass


@app.route('/showmd', methods=['GET'])
def show_markdown():
    filename = request.values.get('filename')
    file_dir=os.path.join(os.getcwd()+'/sync_folder',filename)
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(file_dir, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'text/x-markdown'
            return response
    else:
        pass
@app.route('/user/info', methods=['Get'])
def get_user_info():
    data = {
        'code': 20000,
        "data": {
            'roles': 'admin',
            'name': 'admin',
            'avatar': None
        }
    }
    return data

if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=5000, debug=True)