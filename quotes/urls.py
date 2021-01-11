from django.urls import path
from quotes import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('moi', views.moi, name="moi"),
    path('moi_quick', views.moi_quick, name="moi_quick"),
    path('add_stock', views.add_stock, name="add_stock"),
    path('del_stock/<stock_id>', views.del_stock, name="del_stock"),
    path('modi_stock', views.modi_stock, name="modi_stock"),
    path('youtube', views.youtube, name="youtube"),
    path('facebook', views.facebook, name="facebook"),
    path('wiki_quick', views.wiki_quick, name="wiki_quick"),
    path('wiki', views.wiki, name="wiki"),
    path('dj_test', views.dj_test, name="dj_test"),
    path('login_action', views.login_action, name="login_action"),
    path('event_manage', views.event_manage, name="event_manage"),
    path('search_name', views.search_name, name="search_name"),
    path('guest_manage', views.guest_manage, name="guest_manage"),
    path('view_pdf', views.view_pdf, name="view_pdf"),
    path('save_pdf', views.save_pdf, name="save_pdf"),
]