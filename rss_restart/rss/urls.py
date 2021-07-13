from django.urls import path
from . import views

app_name = 'rss'
urlpatterns = [
    path('', views.CreateFeedView.as_view(), name='index'),
    path('feeds/<int:feed_id>/rss', views.FeedRSSView() , name='feed_rss'),
    path('feeds/<int:pk>', views.FeedDetailView.as_view(), name='feed_detail')
]
