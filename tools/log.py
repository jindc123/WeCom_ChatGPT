import os
from pathlib import Path
import datetime
import logging.config

MEDIA_ROOT = Path(__file__).resolve().parent
LOGGING_DIR = Path(os.getenv("LOG_DIR", str(MEDIA_ROOT / 'logs')))
INFO_LOGGING_DIR = os.path.join(LOGGING_DIR, "info")
ERROR_LOGGING_DIR = os.path.join(LOGGING_DIR, "error")
WARN_LOGGING_DIR = os.path.join(LOGGING_DIR, "warn")

os.makedirs(INFO_LOGGING_DIR, exist_ok=True)
os.makedirs(ERROR_LOGGING_DIR, exist_ok=True)
os.makedirs(WARN_LOGGING_DIR, exist_ok=True)

#  配置日志
logging_config = {
    'version': 1,
    'disable_existing_loggers': False,  # 不使其他日志失效
    'formatters': {  # 日志格式化器
        'default': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '[%(asctime)s] [%(pathname)s:%(lineno)d] '
                      '[%(levelname)s]- %(message)s',
            # '[%(asctime)s] [%(pathname)s:%(lineno)d] [%(levelname)s]- %(message)s',
            # '[%(时间)s] [%(完整文件名)s:%(多少行)d] [%(日志级别)s]- %(自定义内容)s',
        },
    },
    'handlers': {  # 日志处理器
        'console': {  # 标准输出输出
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file': {  # 输出到文件
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 所使用的处理类，这个类可以固定时间开始新的日志，保存原来的日志
            'formatter': 'default',
            'when': "d",  # 时间单位可以是h, d, m , y
            'interval': 1,  # 单位数量，多长时间开始新的记录
            'backupCount': 30,  # 能保存的最大日志文件数量
            'filename': '%s/mylog_info_%s.log ' % (INFO_LOGGING_DIR, datetime.datetime.today().date()),  # 具体日志文件的名字
        },
        'error_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 所使用的处理类，这个类可以固定时间开始新的日志，保存原来的日志
            'formatter': 'default',
            'when': "d",  # 时间单位可以是h, d, m , y
            'interval': 1,  # 单位数量，多长时间开始新的记录
            'backupCount': 30,  # 能保存的最大日志文件数量
            'filename': '%s/mylog_error_%s.log ' % (ERROR_LOGGING_DIR, datetime.datetime.today().date()),  # 具体日志文件的名字
        },
        'warn_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 所使用的处理类，这个类可以固定时间开始新的日志，保存原来的日志
            'formatter': 'default',
            'when': "d",  # 时间单位可以是h, d, m , y
            'interval': 1,  # 单位数量，多长时间开始新的记录
            'backupCount': 30,  # 能保存的最大日志文件数量
            'filename': '%s/mylog_warn_%s.log ' % (WARN_LOGGING_DIR, datetime.datetime.today().date()),  # 具体日志文件的名字
        }
    },
    'loggers': {  # 日志记录器
        'StreamLogger': {
            'handlers': ['console'],  # 所使用的处理器
            'level': 'DEBUG',
        },
        'InfoFileLogger': {
            # 既有 console Handler，还有 file Handler
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'ErrorFileLogger': {
            # 既有 console Handler，还有 file Handler
            'handlers': ['console', 'error_file'],
            'level': 'DEBUG',
        },
        'WarnFileLogger': {
            # 既有 console Handler，还有 file Handler
            'handlers': ['console', 'warn_file'],
            'level': 'DEBUG',
        },
    }
}
# 加载配置
logging.config.dictConfig(logging_config)
# 实例化logger 加载loggers的配置
info_logger = logging.getLogger("InfoFileLogger")
error_logger = logging.getLogger("ErrorFileLogger")
warn_logger = logging.getLogger("WarnFileLogger")
