# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .views import index
from django.conf.urls import url
# Create your tests here.

urlpatterns = [
    url(r'^index/$', index, name="index")
]
