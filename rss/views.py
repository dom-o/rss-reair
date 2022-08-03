from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import edit, detail, list, base
from rss.models import RSSFeed, RSSItem, ConsumableFeed
from rss.forms import RSSForm, ConsumableForm
from django.contrib.syndication.views import Feed
from django.urls import reverse
from datetime import timedelta, date
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return HttpResponse('View create')

# class CreateItemView(edit.FormView):
#     template_name = 'rss/rssitem_form.html'
#     form_class = RSSItemForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         link = form.cleaned_data['link']
#         descr = form.cleaned_data['description']
#
#         feed = RSSFeed.objects.get(id = self.kwargs['pk'])
#         ord = RSSItem.object.filter(feed=feed).count()
#         for ind, link in enumerate(form.cleaned_data['item_links']):
#             ord+=1
#             RSSItem.objects.create(feed=created_feed, content_link = link, title=form.cleaned_data['titles'][ind], description=form.cleaned_data['desc'][ind], ordinal=ord)


class CreateConsumableView(edit.FormView):
    template_name = 'rss/consumable_form.html'
    form_class = ConsumableForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed'] = RSSFeed.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        feed = RSSFeed.objects.get(id = self.kwargs['pk'])
        num_items = form.cleaned_data['daily_items']
        created = ConsumableFeed.objects.create(feed=feed, daily_items=num_items)
        return HttpResponseRedirect(reverse('rss:consumable_detail', kwargs={'pk':created.pk, 'feed_id':created.feed.id}))

class CreateFeedView(edit.FormView):
    template_name = 'rss/rssfeed_form.html'
    form_class = RSSForm

    def form_valid(self, form):
        feed_title = form.cleaned_data['title']
        feed_description = form.cleaned_data['description']

        created_feed = RSSFeed.objects.create(title=feed_title, description=feed_description, length=len(form.cleaned_data['item_links']))

        for ind, link in enumerate(reversed(form.cleaned_data['item_links']) if form.cleaned_data['reverse'] else form.cleaned_data['item_links']):
            RSSItem.objects.create(feed=created_feed, content_link = link, ordinal=ind+1)

        return HttpResponseRedirect(reverse('rss:feed_detail', kwargs={'pk':created_feed.pk}))

class ConsumableDetailView(detail.DetailView):
    model = ConsumableFeed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

delete_age=7
class FeedDetailView(detail.DetailView):
    model = RSSFeed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feed_links = RSSItem.objects.filter(feed=self.object).order_by('ordinal')
        page_number = self.request.GET.get('page')
        pages = Paginator(feed_links, 25)
        context['page_obj'] = pages.get_page(page_number)
        context['total_count'] = pages.count
        return context

class FeedListView(list.ListView):
    model = RSSFeed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feeds = RSSFeed.objects.all().order_by('title')
        page_number = self.request.GET.get('page')
        pages= Paginator(feeds, 25)
        context['page_obj'] = pages.get_page(page_number)
        context['total_count'] = pages.count
        return context

class FeedRSSView(Feed):
    def get_object(self, request, feed_id, pk):
        return ConsumableFeed.objects.filter(feed=feed_id).get(pk=pk)

    def title(self, obj):
        return obj.feed.title

    def link(self, obj):
        return obj.feed.get_absolute_url()

    def description(self, obj):
        return obj.feed.description

    def items(self, obj):
        items = RSSItem.objects.filter(feed=obj.feed)

        if obj.marker <= obj.feed.length:
            return items.filter(ordinal__range=(obj.marker-9,obj.marker)).order_by('ordinal')#[:10]
        else:
            return items.order_by('ordinal')[obj.feed.length-10:obj.feed.length]

    def item_link(self, item):
        return item.content_link

    def item_title(self, item):
        if item.title:
            return item.title
        else:
            return item.content_link

    def item_description(self, item):
        if item.description:
            return item.description
        else:
            return item.content_link
