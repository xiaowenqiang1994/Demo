from math import ceil

from django.core.cache import cache
from django.shortcuts import render, redirect

# Create your views here.
from .models import Post


def post_list(request):
    total = Post.objects.all().count()
    pages = ceil(total / 5)
    page = int(request.GET.get('page', 1))
    start = (page - 1) * 5
    end = start + 5

    posts = Post.objects.all()[start:end]
    return render(request, 'post_list.html',
                  {'posts': posts, 'pages': range(1, pages + 1)})


def post_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        key = 'post-%s' % post.id
        cache.set(key, post)
        return redirect('/post/read/?post_id=%s' % post.id)
    return render(request, 'create_post.html', {})


def post_edit(request):
    if request.method == 'POST':
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        key = 'post-%s' % post_id
        cache.set(key, post)

        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = request.GET.get("post_id")
        post = Post.objects.get(id=post_id)
        return render(request, 'edit_post.html', {'post': post})


def post_read(request):
    post_id = int(request.GET.get('post_id'))
    key = 'post-%s' % post_id
    post = cache.get(key)
    if post is None:
        post = Post.objects.get(id=post_id)
        cache.set(key, post)

    return render(request, 'read_post.html', {'post': post})



