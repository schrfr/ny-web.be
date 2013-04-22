from django.contrib.syndication.views import Feed
from models import Text

class LatestEntries(Feed):
    title = "nY web last entries"
    link = "/articles/1"
    description = "Updates on changes and additions to nY web."
    
    def items(self):
        return Text.objects.exclude(keywords__name="archive").order_by('-pub_date')[:10]
