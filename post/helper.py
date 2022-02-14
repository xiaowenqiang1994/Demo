# coding: utf-8
import time

from redis import Redis
from django.core.cache import cache
from django.conf import settings

from post.models import Post

rds = Redis(**settings.REDIS)


def page_cacha(timeout):
    def wrap1(view_func):
        def wrap2(request, *args, **kwargs):
            key = 'Response-%s' % request.get_full_path()
            response = cache.get(key)
            if view_func.__name__ == 'read_post':
                rds.zincrby('ReadRank', int(request.GET.get('post_id')), 1)
            if response is None:
                response = view_func(request, *args, **kwargs)
                cache.set(key, response, timeout)
                return response
        return wrap2
    return wrap1


def get_top_n(n):
    rank_data = rds.zrevrange('ReadRank', 0, n - 1, withscores=True)
    rank_data = [[int(post_id), int(num)] for post_id, num in rank_data]
    post_id_list = [d[0] for d in rank_data]
    posts = {post.id: post for post in Post.objects.filter(id__in=post_id_list)}
    rank_data = [[posts[post_id], num ] for post_id, num in rank_data]
    return rank_data







def timer(func):
    def wrap(*args, **kwargs):
        t0 = time.time()
        res = func(*args, **kwargs)
        t1 = time.time()
        print(t1 - t0)
        return res
    return wrap

@timer
def foo(n):
    print('start')
    time.sleep(n)
    print('end')


# foo(3)


def bar(n):
    print('start')
    time.sleep(n)
    print('end')


# 普通拆解过程
# fn = timer(bar)
# fn(2)



def timer2(count):
    def wrap1(func):
        def wrap2(*args, **kwargs):
            t0 = time.time()
            for i in range(count):
                res = func(*args, **kwargs)
            t1 = time.time()
            return res
        return wrap2
    return wrap1


# 带参数装饰器的拆解过程
# fn1 = timer2(10)
# fn2 = fn1(bar)
# fn2(0.3)








