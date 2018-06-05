from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from pure_pagination import Paginator,PageNotAnInteger


from .models import Blog, BlogType, BlogTag
from read_views.utls import read_views


# Create your views here.

def blog_pages(request,blogs_all_list):
    try:
        page_num = request.GET.get('page',1)
    except PageNotAnInteger:
        page_num = 1
    p = Paginator(blogs_all_list,5,request=request)
    blogs = p.page(page_num)
    return blogs


def blog_list(request):
    blogs_all_list = Blog.objects.all().order_by('-created_time')

    context = {}
    context['blogs'] = blog_pages(request,blogs_all_list)
    return render(request,'blog/blog_list.html', context)


def blog_detail(request,blog_pk):
    context = {}
    blog = get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key = read_views(request,blog)

    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).first()
    response = render(request,'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key,'true') #阅读cookie标记
    return response

def blogs_with_type(request,blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blog_type_list = Blog.objects.filter(blog_type=blog_type_pk).order_by('-created_time')

    context['blogs'] = blog_pages(request,blog_type_list)
    context['blog_type'] = blog_type
    return render(request,'blog/blog_list.html', context)


def blogs_with_date(request,year,month):
    context = {}
    blog_date_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context['blogs'] = blog_pages(request,blog_date_list)
    return render(request,'blog/blog_list.html',context)

def blogs_with_tag(request,blog_tag_pk):
    context = {}
    blog_tag_list = Blog.objects.filter(blog_tag=blog_tag_pk)
    context['blogs'] = blog_pages(request,blog_tag_list)
    return render(request,'blog/blog_list.html',context)

def search(request):
    context = {}
    searchs = request.GET.get('search','')
    if searchs is not None:
        searchs = Blog.objects.filter(title__icontains=searchs).order_by('-created_time')
    else:
        searchs = Blog.objects.all().order_by('-created_time')
    context['blogs'] = blog_pages(request, searchs)
    return render(request,'blog/blog_list.html',context)





