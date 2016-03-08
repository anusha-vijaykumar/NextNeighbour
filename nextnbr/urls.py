"""nextnbr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from login.views import *
#from django.contrib import user_messages
from profileapp.views import *
from nextnbr.settings import MEDIA_ROOT
from home.views import *
from mail.views import *
# from notification.views import *
#from django_messages.urls import *
#from myapp.views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	# url(r'^show/(?P<notification_id>\d+)/$',show_notification),
	# url(r'^delete/(?P<notification_id>\d+)/$',delete_notification),
	url(r'^homepage/', 'home.views.homepage'),
    url(r'^$', 'django.contrib.auth.views.login'),
	url(r'^friendrequest/$', friendrequest),
    url(r'^addnbrlist/$', addnbrlist),
    url(r'^addnbr/([0-9]*)/$', addnbr),
    url(r'^logout/$', logout_page),
	#url(r'^acceptfrndreq/$', acceptfrndreq),
	url(r'^send_email/$', send_email),
	# url(r'^accounts/login/$', login_page),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home1/$', home_1),
    url(r'^mapview/$', mapview),
    url(r'^msgmap/([0-9]*)/$', msgmap),
    url(r'^viewprofile/$', viewownprofile),
	url(r'^viewfrndprofile/([0-9]*)/$', viewfrndprofile),
    url(r'^viewmapprofile/([0-9]*)/$', viewmapprofile),
	# url(r'^checkproc/$', checkproc),
	url(r'^checkproccur/$', checkproccur),
    url(r'^home/$', home),
	url(r'^home/homepage/$', homepage),
	#url(r'^messages/',django_messages.urls)
	url(r'^home/ho/allfeeds/$', allfeeds),
	url(r'^home/ho/$', ho),
	url(r'^friends/$', friends),
	url(r'^neighbours/$', neighbours),
	url(r'^blocks/$', blocks),
	url(r'^show/$', show),
	#url(r'^msgsuccess/$', msgsuccess),
	url(r'^msgsuccess/$', messages),
	url(r'^next/$', next),
	url(r'^next/([0-9]*)/$', next),
	url(r'^frequest/([0-9]*)/$', frequest),
	url(r'^msg/([0-9]*)/$', msg),
	url(r'^togo/([0-9]*)/$', togo),
    url(r'^go/([0-9]*)/$', go),
    url(r'^nbrfeeds/([0-9]*)/$', to),
#     url(r'^to/([0-9]*)/$', to),
	url(r'^oo/([0-9]*)/$', oo),
	url(r'^reply/([0-9]*)/$', reply),
	url(r'^blockthreads/$', blockthreads),
	url(r'^allthreads/$', allthreads),
	url(r'^neighbourhoodthreads/$', neighbourhoodthreads),
	url(r'^neighbourthreads/$', neighbourthreads),
	url(r'^friendthreads/$', friendthreads),
	#url(r'^home/ho/msgsuccess/$',messages),
	url(r'^newmsg/$', newmsg),
	url(r'^message/$', message),
	url(r'^newms/$', newms),
	url(r'^acceptfrndreq/([0-9]*)$', acceptfrndreq),
	url(r'^sendblkreq/([0-9]*)$', sendblkreq),
    url(r'^unjoinblkreq/([0-9]*)$', unjoinblkreq),
	url(r'^acceptblkreq/([0-9]*)$', acceptblkreq),
	url(r'^declinefrndreq/([0-9]*)$', declinefrndreq),
	url(r'^notifications/$', notifications),
	#url(r'^getid/$', getid),
	url(r'^accounts/profile/$', profile),
#     url(r'^blockrequest/$', blockrequest),
	url(r'^newestmessage/$', newestmessage),
	url(r'^blknbrmsg/$', blknbrmsg),
	url(r'^replymessage/$', replymessage),
    url(r'^search/$', search),
#     url(r'^viewmsg/$', viewmsg),      
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': MEDIA_ROOT}),
] 
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
