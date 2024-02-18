import os
import logging
from logging.handlers import TimedRotatingFileHandler

class LogManager:

    LOG_INFO = logging.INFO
    LOG_DEBUG = logging.DEBUG
    LOG_WARNING = logging.WARNING
    LOG_ERROR = logging.ERROR
    LOG_CRITICAL = logging.CRITICAL

    APP_ERROR_LOG = 'app_error'
    
    # static 變數，用於儲存所有 logger
    loggers = {}

    def __init__(self, log_name, level=logging.INFO):

        if log_name in LogManager.loggers:
            self.logger = LogManager.loggers[log_name]
        else:
            log_directory = os.path.join('writable', 'logs')
            self.logger = logging.getLogger(log_name)
            self.logger.setLevel(level)

            os.makedirs(log_directory, exist_ok=True)
            log_filename = os.path.join(log_directory, f'{log_name}.log')

            # 創建一個 handler，每天輪換一次，保留三天的日誌
            handler = TimedRotatingFileHandler(log_filename, when="D", interval=1, backupCount=3)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            # 為 logger 添加 handler
            self.logger.addHandler(handler)

    # 寫入 log
    def write(self, msg, level=logging.INFO):
        self.logger.log(level, msg)

    # 取得 logger 實體
    @staticmethod
    def get_logger(log_name, level=logging.INFO)->'LogManager':
        if log_name not in LogManager.loggers:
            LogManager.loggers[log_name] = LogManager(log_name, level)
        return LogManager.loggers[log_name]

    # 直接寫入系統錯誤 log
    @staticmethod
    def write_error_log(msg):
        error_log = LogManager.get_logger(LogManager.APP_ERROR_LOG, LogManager.LOG_ERROR)
        error_log.error(msg)
