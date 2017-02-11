from django.conf.urls import url

from . import views


app_name = 'main' 
#This sets application namespace to diffretiate urls of different apps.

urlpatterns = [
    #url for home-page:
    url(r'^$', views.index, name='index'),
    #url for login-page:
    url(r'^login$', views.login, name='login'),
    #url for signup-page:
    url(r'^signup$', views.signup, name='signup'),

    #url to log in a user:
    url(r'^log_req$', views.logInReq, name='login_req'),
    
    #url for create-user:
    url(r'^register_user$', views.register, name='register_user'),

    #url for logged-in:
    #url(r'(?P<pk>[0-9]+)/logged_in/$',views.LoggedIn.as_view(),name='loggedin'),

    #url for logout:
    url(r'^logout$', views.logout, name='logout'),

    #url to search a topic:
    url(r'^search$', views.search, name='search'),

    url(r'^search1$', views.search1, name='search1'),

    #url to search a topic:
    url(r'^search_checkup$', views.search_checkup, name='search_checkup'),

    url(r'^quest$', views.quest, name='quest'),
]
