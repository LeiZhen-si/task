import os
import time

# Prod config file
basedir = os.path.abspath(os.path.dirname(__file__))


class DbConf:
    URL = "http://localhost:8086"
    TOKEN = "HvqS1LSlGHVeEYcXMl44pu6FGlBJw8qM7QFiDGdblaZvR5mkfUVuaNYoIVwho7lYPWdsrj4mxMydaLiO3T3uwQ=="
    ORG = "SDC"
    BUCKET = "sdc_task_01"

class LogConf:
    LOGPATH = "logs"
    LOGNAME = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    LOGFORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s"
    LOGLEVEL = "INFO"

class SyncDir:
    # BASEABSPATH = "/home/sssbjlx205/Documents/workspace/Node-red/validation-tool/task/flask-vue-crud/server/tasks" # 共享同步目录的绝对路径
    BASEABSPATH = "/usr/src/app/tasks"
    BASETASKPATH = BASEABSPATH + "/tasks" # 该目录下存储的都是task 的报告，以task_name 为区分,遍历这个文件夹，找到所有的报告文件

class ProductionConfig(DbConf,LogConf,SyncDir):
    pass