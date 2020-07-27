from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('moi', views.moi, name="moi"),
    path('add_stock', views.add_stock, name="add_stock"),
    path('del_stock/<stock_id>', views.del_stock, name="del_stock"),
    path('modi_stock', views.modi_stock, name="modi_stock"),
    path('youtube', views.youtube, name="youtube"),
    path('facebook', views.facebook, name="facebook"),
    path('wiki_quick', views.wiki_quick, name="wiki_quick"),
    path('wiki', views.wiki, name="wiki"),
]