from django.conf.urls import url

from cmp_Price import views
urlpatterns = [
    url(r'^home/', views.home),
    url(r'^search/', views.search,name='postKey'),
]
