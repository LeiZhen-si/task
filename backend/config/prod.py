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
    BASE_ABS_PATH = "/usr/src/app" # 共享同步目录的绝对路径
    BASE_TASK_PATH = BASE_ABS_PATH + "/tasks" # 该目录下存储的都是task 的报告，以task_name 为区分
    BASE_WARM_PATH = BASE_ABS_PATH + "/warms"  # 该目录下存储的都是warms 的报告，以task_name 为区分

class ProductionConfig(DbConf,LogConf,SyncDir):
    pass