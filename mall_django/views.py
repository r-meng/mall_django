from datetime import datetime

from django.shortcuts import render

from accounts.models import User
from system.models import Slider, News
from utils import constants


def index(request):
    """首页"""
    # 查询轮播图
    slider_list = Slider.objects.filter(types=constants.SLIDER_TYPE_INDEX)

    # 首页新闻
    now_time = datetime.now()
    news_list = News.objects.filter(types=constants.NEWS_TYPE_NEWS,
                                    is_top=True,
                                    is_valid=True,
                                    start_time__lte=now_time,
                                    end_time__gte=now_time)
    # user_id = request.session[constants.LOGIN_SESSION_ID]
    # print(user_id)
    # user = User.objects.get(pk=user_id)
    # # if not user_id:
    # #     return 403
    return render(request, 'index.html', {
        'slider_list': slider_list,
        'news_list': news_list,
        # 'user': user
    })