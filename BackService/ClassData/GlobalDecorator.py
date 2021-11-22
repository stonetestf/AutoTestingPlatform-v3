from functools import wraps
from rest_framework.authtoken.models import Token as db_Token


# 全局装饰器
class GlobalDer(object):
    def user_state(self, func):
        @wraps(func)
        def isToken(*args, **kwargs):
            a = func(*args, **kwargs)
            content = {}
            try:
                obj_db_Token = db_Token.objects.filter(key=args[0].META['HTTP_TOKEN'])  # 从请求中获取数据，查询token
                # content = json.loads(a.content)
                # a.content = json.dumps(content)
            except BaseException as e:
                content['errorMsg'] = "Request Hearders Not TOKEN"
                a.status_code = 500
            else:
                pass
            return a

        return isToken
