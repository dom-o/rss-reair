from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import edit, detail, ListView
from rss.models import RSSFeed, RSSItem
from rss.forms import RSSForm
from django.contrib.syndication.views import Feed
from django.urls import reverse
from datetime import timedelta, date
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return HttpResponse('View create')


class CreateFeedView(edit.FormView):
    template_name = 'rss/rssfeed_form.html'
    form_class = RSSForm

    def form_valid(self, form):
        feed_title = form.cleaned_data['title']
        feed_description = form.cleaned_data['description']
        num_items = form.cleaned_data['daily_items']
        created_feed = RSSFeed.objects.create(title=feed_title, description=feed_description, daily_items=num_items)

        for link in form.cleaned_data['item_links']:
            RSSItem.objects.create(feed=created_feed, content_link = link)

        return HttpResponseRedirect(reverse('rss:feed_detail', kwargs={'pk':created_feed.pk}))


delete_age=7
class FeedDetailView(detail.DetailView):
    model = RSSFeed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['live_count'] = RSSItem.objects.filter(feed=self.object, live=True).count()
        context['total_count'] = RSSItem.objects.filter(feed=self.object).count()

        if(context['live_count'] == context['total_count']):
            context['final_item_date'] = RSSItem.objects.latest('live_date').live_date
        else:
            context['final_item_date'] = date.today() + timedelta(days=(context['total_count']-context['live_count']) / self.object.daily_items)

        feed_links = RSSItem.objects.filter(feed=self.object).order_by('-live_date')
        page_number = self.request.GET.get('page')
        context['page_obj'] = Paginator(feed_links, 25).get_page(page_number)

        context['delete_date'] = context['final_item_date'] + timedelta(days=delete_age)
        return context


class FeedRSSView(Feed):
    def get_object(self, request, feed_id):
        return RSSFeed.objects.get(pk=feed_id)

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return obj.description

    def items(self, obj):
        return RSSItem.objects.filter(feed=obj).filter(live=True).order_by('-live_date')[:10]

    def item_link(self, item):
        return item.content_link

# def createNewFeed(request):
#     feed_title = request.POST['title'] if 'title' in request.POST else ''
#     feed_description = request.POST['description'] if 'description' in request.POST else ''
#
#     created_feed = RSSFeed.objects.create(title=request.POST['title'], description=request.POST['description'])
#
#     item_links = request.POST['items'].splitlines() if 'items' in request.POST else []
#     if item_links:
#         for link in item_links:
#             #todo: validate each link, if not valid send error indicating which link is wrong
#             try:
#                 URLValidator()(link)
#                 RSSItem.objects.create(feed = created_feed, content_link=link)
#             except ValidationError:
#                 print(link)
#
#         return HttpResponseRedirect(reverse('rss:feed_detail', kwargs={'pk':created_feed.pk}))
#     else:
#         print('No items for in feed.')
#         return HttpResponseBadRequest('<p>No items in feed. Include items, one url per line.</p><a href="/">go back</a>/')
