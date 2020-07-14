from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, get_object_or_404

# Create your views here.
from system.models import News
from utils import constants
from utils.verify import VerifyCode


def news_list(request, template_name='news_list.html'):
    page = request.GET.get('page', 1)
    page_size = 20

    news_list = News.objects.filter(types=constants.NEWS_TYPE_NEWS,
                               is_valid=True)
    paginator = Paginator(news_list, page_size)
    page_data = paginator.page(page)
    return render(request, template_name, {
        'page_data': page_data
    })


def news_detail(request, pk, template_name='news_info.html'):
    news_obj = get_object_or_404(News, pk=pk, is_valid=True)
    news_obj.view_count = F('view_count') + 1
    news_obj.save()
    news_obj.refresh_from_db()
    return render(request, template_name, {
        'news_obj': news_obj
    })


def verify_code(request):
    client = VerifyCode(request)
    return client.gen_code()
