from rss.models import RSSFeed, RSSItem
from celery import shared_task
from django.db.models import Q, F, Count, Max
from rss.views import delete_age
from datetime import timedelta, date

@shared_task
def test_task():
    print('yoo')

@shared_task
def set_live(item_id):
    item = RSSItem.objects.get(id=item_id)
    item.live= True
    item.save()

@shared_task
def get_items(feed_id, dailies):
    items = RSSItem.objects.filter(feed=feed_id, live=False)[:dailies]
    for item in items:
        set_live.delay(item.id)

#run daily
@shared_task
def publish():
    feeds = RSSFeed.objects.all()
    for feed in feeds:
        get_items.delay(feed.id, feed.daily_items)

#run daily
@shared_task
def clear_old_feeds():
    RSSFeed.objects  \
        .annotate(live_count=Count('rssitem', filter=Q(rssitem__live=True)))  \
        .annotate(total_count=Count('rssitem'))  \
        .filter(live_count=F('total_count'))  \
        .annotate(latest_live=Max('rssitem__live_date'))  \
        .filter(latest_live__lte=date.today()-timedelta(days=delete_age))  \
        .delete()
