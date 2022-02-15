# coding: utf-8
import time
from django.utils.deprecation import MiddlewareMixin


class BlockMiddleware(MiddlewareMixin):
    def proess_request(self, request):
        request_time = request.session.get('request_time', [0, 0])
        now = time.time()
        if now - request_time[0] < 4:
            time.sleep(10)  # 访问太频繁，阻塞
            # 更新时间列表
            request_time = [request_time[1], time.time()]
        else:
            request_time = [request_time[1], now]
        request.session['request_time'] = request_time    # 将时间列表存回 session

