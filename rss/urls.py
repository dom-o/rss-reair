from django.urls import path
from . import views

app_name = 'rss'
urlpatterns = [
    path('', views.CreateFeedView.as_view(), name='index'),
    path('list', views.FeedListView.as_view(), name='feed_list' ),
    path('<int:pk>', views.FeedDetailView.as_view(), name='feed_detail'),
    path('<int:pk>/createfeed', views.CreateConsumableView.as_view(), name='create_consumable'),
    # path('<int:feed_id>/additem', views.CreateItemView.as_view(), name='create_item')
    path('<int:feed_id>/feeds/<int:pk>', views.ConsumableDetailView.as_view() , name='consumable_detail'),
    path('<int:feed_id>/feeds/<int:pk>/feed', views.FeedRSSView() , name='feed_rss'),

]
