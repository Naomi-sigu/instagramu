from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views
# from django.urls import path, include

urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url(r'^search/$',views.search,name='search'),
    url(r'^post_profile/(?P<pk>\d+)$',views.others_profile,name='others_profile'),
]    
 
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)