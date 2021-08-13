from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator

# Create your models here.
class RSSFeed(models.Model):
    title = models.TextField()
    description = models.TextField(blank=True, default='')
    daily_items = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    date_created = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('rss:feed_detail', kwargs={'pk':self.pk})

    def get_rss_url(self):
        from django.urls import reverse
        return self.get_absolute_url() + '/rss'


class RSSItem(models.Model):
    live = models.BooleanField(default=False)
    feed = models.ForeignKey('RSSFeed', on_delete=models.CASCADE)
    live_date = models.DateField(auto_now=True)
    content_link = models.TextField(validators=[URLValidator()])
