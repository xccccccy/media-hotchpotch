import logging
import logging.handlers

import os

pwd = os.getcwd()

if not os.path.exists('logs/root.log'):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    with open('logs/root.log', 'w', encoding='utf-8') as fp:
        pass


def register_logging(app):
    # 设置日志记录器的的记录等级，级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG
    app.logger.setLevel(logging.DEBUG)

    # 设置输出到文件的时间格式
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    # 设置日志处理器，实例化这个类传入日志文件的目标路径、最大文件尺寸和备份数量。当日志大小超过maxBytes时，会创建新的日志文件。# when='midnight'
    # backupCount为最大的日志文件数，当日志文件数超过最大日志数时，后面的日志记录会从第一个文件末尾开始写，并覆盖最前面的记录。
    file_handler = logging.handlers.RotatingFileHandler(os.path.join(pwd, 'logs/root.log'), maxBytes=10 * 1024 * 1024, backupCount=1)
    # 应用设置输出的日志格式
    file_handler.setFormatter(formatter)
    # 设置接受日志的等级
    file_handler.setLevel(logging.DEBUG)
    # 注册日志处理器
    app.logger.addHandler(file_handler)
