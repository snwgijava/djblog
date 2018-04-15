import datetime

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from read_views.models import ReadNum, ReadDetail




def read_views(request,obj):
    '''
    对记录+1
    :param request:
    :param obj:
    :return:
    '''
    ct = ContentType.objects.get_for_model(obj)
    key = "{0}_{1}_read".format(ct.model,obj.pk)
    if not request.COOKIES.get(key):
        #get_or_create方法是按条件查询，查询不到就创建
        #总阅读+1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # 计数+1
        readnum.read_num += 1
        readnum.save()

        #当前阅读数+1
        date = timezone.now().date()
        readDetail,created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key


def get_seven_days_read_data(content_type):
    '''
    获取到每天的访问量
    :param content_type:
    :return:
    '''
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        #获取某个Model的每天的访问数
        readDetail = ReadDetail.objects.filter(content_type=content_type,date=date)
        #将日期相同的一天的访问量相加
        result = readDetail.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates,read_nums

def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num')[:7]
    return read_details



