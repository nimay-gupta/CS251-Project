from . import views
from django.contrib import admin
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^ajax/get_response/$', views.answer_me, name='get_response'),
]
