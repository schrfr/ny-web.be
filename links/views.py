from models import Link, LinkCategory
from django.shortcuts import render_to_response
from django.template import RequestContext


def links(request):
    """
    Link view.
    Retrieves all the bookmarks sorted by their category.
    """
    links = Link.objects.all().order_by('category')
    return render_to_response('links.html', {'links': links}, context_instance=RequestContext(request))