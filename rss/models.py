from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.urls import reverse

# Create your models here.
class RSSFeed(models.Model):
    title = models.TextField()
    description = models.TextField(blank=True)
    length = models.PositiveIntegerField()
    def get_absolute_url(self):
        return reverse('rss:feed_detail', kwargs={'pk':self.pk})

class ConsumableFeed(models.Model):
    feed = models.ForeignKey('RSSFeed', on_delete=models.CASCADE)
    marker = models.PositiveIntegerField(default=0)
    daily_items = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    # date_created = models.DateField(auto_now_add=True)
    # date_modified = models.DateField(auto_now=True)
    def get_absolute_url(self):
        return reverse('rss:consumable_detail', kwargs={'pk':self.pk, 'feed_id':self.feed.id})

    def get_rss_url(self):
        return reverse('rss:feed_rss', kwargs={'pk':self.pk, 'feed_id':self.feed.id})

class RSSItem(models.Model):
    #allow the user to add a list of own titles/descs
    #or default description to nothing and title to url

    ordinal = models.PositiveIntegerField()
    feed = models.ForeignKey('RSSFeed', on_delete=models.CASCADE)
    content_link = models.TextField(validators=[URLValidator()])
    description = models.TextField(blank=True)
    title = models.TextField(blank=True)
