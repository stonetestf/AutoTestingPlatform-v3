from django_redis import get_redis_connection
from ClassData.Logger import Logging as cls_Logging


class RedisHandle(cls_Logging):
    def witer_type_dict(self, label, key, value, timeOut=None):
        """
        :param label: '标记':{'k':'v','k':v}
        :param key:
        :param value:
        :param timeOut:为空时永久保存
        :return: True or False
        """
        try:
            conn = get_redis_connection("default")  # 连接
            conn.hset(label, key, value)
            if timeOut:
                conn.expire(label, timeOut)  # expire函数设置过期时间为秒
        except BaseException as e:
            cls_Logging.print_log(self,'error','Redis>witer_type_dict',e)
            cls_Logging.record_error_info(self,'ALL', 'ClassData', 'Redis>witer_type_dict', e)
            return False
        else:
            return True
