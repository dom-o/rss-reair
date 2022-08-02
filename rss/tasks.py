from rss.models import ConsumableFeed
from celery import shared_task
from django.db.models import F
from rss.views import delete_age

@shared_task
def test_task(self):
    print(f'Request: {self.request!r}')

@shared_task
def update_marker(feed_id):
    feed = ConsumableFeed.objects.get(id=feed_id)
    # print(f'{feed.marker}+{feed.daily_items}={feed.marker+feed.daily_items}')
    feed.marker += feed.daily_items
    feed.save()

#run daily
@shared_task
def publish():
    feeds = ConsumableFeed.objects.all()
    for feed in feeds:
        update_marker.delay(feed.id)


#run daily
@shared_task
def clear_old_feeds():
    objs=ConsumableFeed.objects.filter(marker__gte=delete_age*F('daily_items')+F('feed__length')).delete()
    # for object in objs:
    #     print(object.feed.length, object.marker, object.daily_items)
    #     print(object.marker >= delete_age*object.daily_items+object.feed.length)
