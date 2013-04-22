# Views not belonging to any app

from django.shortcuts import render_to_response
from django.template import RequestContext
import feedparser
from people.models import Person


def dereactor(request):
    """
    De Reactor view.
    Retrieves the last entries from de Reactor RSS feed.
    """
    channels = feedparser.parse('http://www.dereactor.org/embeds/rss_kritieken/')    
    return render_to_response('dereactor.html', { 'channels': channels }, context_instance=RequestContext(request))


def about(request, iso_code):
    """
    About view.
    Captures the ISO code in the URL and passes it to the template.
    """
    my_dict = {
        'iso_code'   : iso_code, 
        'author_list': Person.objects.filter(authors_set__isnull=False).distinct(), 
    }
    return render_to_response('about.html', my_dict, context_instance=RequestContext(request))
