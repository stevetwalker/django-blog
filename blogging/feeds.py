"""blogging/feeds.py"""

from django.contrib.syndication.views import Feed
from django.urls import reverse

from blogging.models import Post

class LatestPostsFeed(Feed):
    title = "Blog feed"
    link = "/blog-feed/"
    description = "A feed of posts to feed your journey of enlightenment."

    def items(self):
        published = Post.objects.exclude(published_date__exact=None)
        posts = published.order_by('-published_date')

        # Return the three most recent posts
        return posts[:3]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text

    def item_link(self, item):
        return reverse('blog_detail', args=[item.pk])
