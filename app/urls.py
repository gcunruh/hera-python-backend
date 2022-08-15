from django.urls import path, re_path
from app import views

urlpatterns = [ 
    re_path(r'^api/funds$', views.fund_list),
    re_path(r'^api/fund$', views.create_fund),
    re_path(r'^api/subscriber/(?P<pub_key>[a-zA-Z0-9_.-]+)$', views.subscriber_detail),
    re_path(r'^api/enroll$', views.enroll),
    re_path(r'^api/claim$', views.claim),
    re_path(r'^api/create$', views.create_image),
    re_path(r'^api/createmetadata$', views.create_metadata)
]
