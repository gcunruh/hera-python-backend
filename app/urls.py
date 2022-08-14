from django.urls import path
from django.conf.urls import url 
from app import views

urlpatterns = [ 
    url(r'^api/funds$', views.fund_list),
    url(r'^api/subscriber/(?P<pub_key>[a-zA-Z0-9_.-]+)$', views.subscriber_detail),
    url(r'^api/enroll$', views.enroll),
    url(r'^api/claim$', views.claim),
]
