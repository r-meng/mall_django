from django.http import HttpResponse

from accounts.models import User


def ip_middleware(get_response):


    def middleware(request):

        # 请求到达前的业务逻辑
        print('请求到达前的业务逻辑')
        # 请求不满足业务规则：IP被限制
        ip = request.META.get('REMOTE_ADDR', None)
        ip_disable_list = [
            '127.0.0.2'
        ]
        # for ip_dis in ip_disable_list:
        #     if ip_dis == ip:
        if ip in ip_disable_list:
            return HttpResponse('not allowed')
        response = get_response(request)

        # 视图函数调用之后的业务逻辑
        print('视图函数调用之后的业务逻辑')
        return response

    return middleware


class MallAuthMiddleware(object):
    """ 自定义的登录验证中间件 """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        print('MallAuthMiddleware请求到达前的业务逻辑')
        # 请求不满足业务规则：IP被限制

        user_id = request.session.get('user_id', None)
        if user_id:
            user = User.objects.get(pk=user_id)
        else:
            user = None

        request.my_user = user
        response = self.get_response(request)

        # 视图函数调用之后的业务逻辑
        print('MallAuthMiddleware视图函数调用之后的业务逻辑')
        return response
