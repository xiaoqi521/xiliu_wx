# -*- coding: utf-8 -*-
from django.conf.urls import url

from wx_api import views


urlpatterns = [
    url(r'^apply?$',
        views.ApplyForViews.as_view(), name='apply'),

]