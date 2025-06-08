import logging
from logging.handlers import RotatingFileHandler


# Настройка ротации логов
file_handler = RotatingFileHandler('bot_logs.log',
                                   maxBytes=100*1024*1024,  # 100MB
                                   backupCount=5,
                                   encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(),
              file_handler]
)
