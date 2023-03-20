import redis
from tools.log import info_logger, error_logger
from tools.get_config import getConfig


class RedisClient:
    REDIS_HOST = getConfig("gpt.conf", 'redis', 'REDIS_HOST')
    REDIS_PORT = getConfig("gpt.conf", 'redis', 'REDIS_PORT')
    REDIS_DB = getConfig("gpt.conf", 'redis', 'REDIS_DB')
    REDIS_PASSWORD = getConfig("gpt.conf", 'redis', 'REDIS_PASSWORD')
    CODE_REDIS_KEY = "wecom_gpt_code_"
    TOKEN_REDIS_KEY = "wecom_gpt_token_"

    def __init__(self, db=None):
        try:
            if self.REDIS_PASSWORD:
                self.__conn = redis.Redis(connection_pool=redis.BlockingConnectionPool(
                    decode_responses=True,
                    timeout=5,
                    socket_timeout=5,
                    password=self.REDIS_PASSWORD,
                    host=self.REDIS_HOST,
                    port=self.REDIS_PORT,
                    db=self.REDIS_DB if not db else db))
            else:
                self.__conn = redis.Redis(connection_pool=redis.BlockingConnectionPool(
                    decode_responses=True,
                    timeout=5,
                    socket_timeout=5,
                    host=self.REDIS_HOST,
                    port=self.REDIS_PORT,
                    db=self.REDIS_DB))
        except Exception as e:
            error_logger.error(f'Redis连接失败 {e}')

    def set(self, key, data, ex=60):
        try:
            self.__conn.set(key, data, ex)
        except Exception as e:
            error_logger.error(f'Redis set失败 {e}')

    def get(self, key):
        try:
            r = self.__conn.get(key)
            return r
        except Exception as e:
            error_logger.error(f'Redis  get失败 {e}')

    def delete(self, key):
        try:
            self.__conn.delete(key)
        except Exception as e:
            error_logger.error(f'Redis  delete失败 {e}')
