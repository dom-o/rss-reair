from rss.models import RSSFeed, RSSItem
from celery import shared_task
from django.db.models import Q, F, Count, Max
from rss.views import delete_age
from datetime import timedelta, date

#run daily
@shared_task
def publish():
    feeds = RSSFeed.objects.all()
    for feed in feeds:
        items = RSSItem.objects.filter(feed=feed, live=False)[:feed.daily_items]
        for item in items:
            item.live = True
            item.save()

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
