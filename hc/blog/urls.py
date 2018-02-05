from django.conf.urls import url
from . import views

urlpatterns = [
     url(r'^$', views.blog_category, name="hc-category"),
    #  url(r'^create/$', views.create_blog, name="hc-blog"),
     url(r'^blog/view/(?P<slug>\s+)/$', views.view_blog_detail, name='view_blog_post')
 ]