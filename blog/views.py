import datetime
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from djangoBlog.models import Blog
from read_views.utls import get_seven_days_read_data,get_today_hot_data


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today,read_details__date__gt=date)\
        .values('id','title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')[:7]
    return blogs


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates,read_nums = get_seven_days_read_data(blog_content_type)

    #获取七天热门文章的缓存数据
    hot_data_for_7_days = cache.get('hot_data_for_7_days')
    if hot_data_for_7_days is None:
        hot_data_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_data_for_7_days',hot_data_for_7_days,3)

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_date'] = get_today_hot_data(blog_content_type)
    context['hot_data_for_7_days'] = hot_data_for_7_days
    return render_to_response('home.html',context)