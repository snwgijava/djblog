from django.shortcuts import render_to_response,get_object_or_404
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from .models import Blog,BlogType
# Create your views here.

def blog_list(request):

    blogs_all_list = Blog.objects.all()
    try:
        page_num = request.GET.get('page',1)
    except PageNotAnInteger:
        page_num = 1
    p = Paginator(blogs_all_list,5,request=request)
    blogs = p.page(page_num)
    context = {}
    context['blogs'] = blogs
    # context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html', context)


def blog_detail(request,blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog,pk=blog_pk)
    return render_to_response('blog/blog_detail.html', context)

def blogs_with_type(request,blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blog_type_list = Blog.objects.filter(blog_type=blog_type_pk)
    try:
        page_num = request.GET.get('page',1)
    except PageNotAnInteger:
        page_num = 1
    p = Paginator(blog_type_list,5,request=request)
    blogs = p.page(page_num)
    context['blogs'] = blogs
    context['blog_type'] = blog_type
    return render_to_response('blog/blogs_with_type.html', context)


