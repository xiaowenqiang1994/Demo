from django.shortcuts import render, redirect

# Create your views here.
from .models import Post

def post_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    return render(request, 'create_post.html', {})


def post_edit(request):
    if request.method == 'POST':
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = request.GET.get("post_id")
        post = Post.objects.get(id=post_id)
        return render(request, 'edit_post.html', {'post': post})


def post_read(request):
    post_id = int(request.GET.get('post_id'))
    post = Post.objects.get(id=post_id)
    return render(request, 'read_post.html', {'post': post})


def post_list(request):

    return render(request, 'list_post.html', {})

