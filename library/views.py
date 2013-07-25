# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.template import RequestContext

from django.views.generic.list_detail import object_list
from django.db.models import Q

import datetime

from models import Zone, StickyText, Keyword, DocumentType, Text, Language
from people.models import Person


def text(request, category, slug):
    """
    Text view.
    Retrieves a text matching a given category/slug pair.
    """
    view = request.GET.get('view', 'none')
    cp = request.GET.get('cp', None)
    try: cp = int(cp)
    except: pass
    cc = request.GET.get('cc', None)
    try: cc = int(cc)
    except: pass
    ct = request.GET.get('ct', None)
    try: ct = int(ct)
    except: pass
    zone = get_object_or_404(Zone, identifier=category)
    path = u"%s" % zone
    path = u"%s%s/" % (path[0].capitalize(), path[1:])
    text = get_object_or_404(Text, zone__identifier=category, identifier=slug)
    
    # Only authenticated users get to access unpublished texts:
    if not text.publish or text.future():
        if not request.user.is_authenticated():
            raise Http404
    
    related_texts = Text.objects.filter(from_texts__from_text__identifier=text.identifier).order_by('-pub_date')
    
    ctx = {
        'text': text, 
        'related_text_list': related_texts, 
        'view': view, 
        'cp': cp, 
        'cc': cc, 
        'ct': ct, 
        'path': path 
    }
    
    return render_to_response('text.html', ctx, context_instance=RequestContext(request))


def timeline(request):
    """
    Timeline view.
    Retrieves:
    * the texts posted within the last n days.
    * the stickies for each category
    """
    today = datetime.date.today()
    oldest = today - datetime.timedelta(days=150)
    text_list = Text.objects.filter(pub_date__gte=oldest).order_by('-pub_date')
    if not request.user.is_authenticated():
        # Only authenticated users get to see future posts and draft posts
        text_list = text_list.filter(publish=True).filter(pub_date__lte=today)
    stickies = StickyText.objects.all()
    try:
        extra_context = {
            'stickies_showtime': stickies.get(zone__identifier='showtime'),
            'stickies_untimely_meditations': stickies.get(zone__identifier='untimely-meditations'),
            'stickies_transitzone': stickies.get(zone__identifier='transitzone'),
            'stickies_long_hard_looks': stickies.get(zone__identifier='long-hard-looks'),
        }
    except:
        extra_context = {}
    
    return object_list(
        request, 
        queryset = text_list,
        template_name = 'timeline.html',
        template_object_name = 'text',
        extra_context = extra_context,
    )


def search(request):
    """
    Search view.
    retrieves the texts containing the query (insentive search) in:
    * their title
    * their description
    * their body
    """
    if request.method == 'GET': # If the search form has been submitted...        
        query = request.GET.get('query', '')
        if query.isspace() or query == '':
            text_list = Text.objects.none()
            extra_context = {
                'path'    : u"Search/",
                'subpath' : u"You've searched for nothing!",
            }
        else:
            text_list = Text.objects.filter(
                            Q(title__icontains=query) | 
                            Q(description__icontains=query) | 
                            Q(body__icontains=query) |
                            Q(authors__first_name__icontains=query) |
                            Q(authors__last_name__icontains=query)
                        ).order_by('-pub_date')
            extra_context = {
                'path'    : u"Search/",
                'subpath' : u"You've searched on “%s”" % query,
            }
    else:
        text_list = Text.objects.none()
        extra_context = {
            'path'    : u"Search/",
            'subpath' : u"You've searched for nothing!",
        }
    
    return object_list(
        request, 
        queryset = text_list,
        template_name = 'list.html',
        template_object_name = 'text',
        extra_context = extra_context,
    )


def list_new(request, **kwargs):
    """
    Archiev List view.
    Retrieves the texts for a given field
    """
    
    archive = kwargs.get('archive')
    field = kwargs.get('field')
    query = kwargs.get('query')
    category = kwargs.get('category')
    
    # blurps = {
    #     'showtime' : 'In showtime we bring you the news, we announce debates and we \
    #                   give insights into the flemish field of literature. The latest, \
    #                   the hottest, the juiciest.',
    #     'untimely-meditations' : 'In Untimely meditations we meditate on certain topics. \
    #                   Different authors are given free credits to bring in texts.',
    #     'transitzone' : 'We focus on the translation of texts into different languages. \
    #                   As a way to open up the boundaries, to broaden our perspectives.',
    #     'long-hard-looks' : 'In long hard looks we look.',
    # }
    
    blurps = {
        'showtime' : u'Actualiteit, aankondigingen, aanvullingen op nY-print, debat en andere interventies.',
        'untimely-meditations' : u'Korte reflecties, ontstaan bij lectuur, beelden of andere aanleidingen, \
            niet noodzakelijk gelinkt met het ‘actuele debat’. Centraal staan de kwaliteit van de reflectie, \
            het profiel van de auteurs, hun specifieke invalshoeken en fascinaties.',
        'transitzone' : u'Texts related to the literary journal <em>nY</em> or its predecessors <em>yang and freespace \
            Nieuwzuid</em>, made available in other languages. Please contact us at \
            <a href="mailto:info@ny-web.be">info@ny‑web.be</a> \
            if you\'d like to publish one of these texts or need more information. Feel free to link!',
        'long-hard-looks' : u'Kritische essays uit nY, yang en freespace Nieuwzuid. Groeiend archief.',
    }
    
    extra_context = {}
    
    if archive: # All zones mixed
        template_name = 'archive.html'
        texts = Text.objects.filter(publish=True).order_by('-pub_date')
        path = u"Web Archive/"
        extra_context['path'] = path
    
    else: # Per zone lists
        template_name = 'list.html'
        # Raise an error if the zone doesn't exist
        texts = Text.objects.filter(zone__identifier=category).filter(publish=True).order_by('-pub_date')
        zone = get_object_or_404(Zone, identifier=category)
        extra_context['zone'] = zone
        path = u"%s%s/" % (zone.name[0].capitalize(), zone.name[1:])
        extra_context['path'] = path
        if category in blurps:
            extra_context['blurp'] = u"%s" % blurps[category]
    
    if field != None:
        if field == 'tag':
            texts = texts.filter(publish=True).filter(keywords__identifier=query)
            extra_context['path'] += u"Tag/%s/" % get_object_or_404(Keyword, identifier=query)
        
        elif field == 'author':
            texts = texts.filter(publish=True).filter(authors__slug=query)
            extra_context['path'] += u"Author/%s/" % get_object_or_404(Person, slug=query)
        
        elif field == 'type':
            texts = texts.filter(publish=True).filter(document_type__identifier=query)
            extra_context['path'] += u"Type/%s/" % get_object_or_404(DocumentType, identifier=query)
        
        elif field == 'language':
            texts = Text.objects.filter(publish=True).filter(language__identifier=query)
            extra_context['path'] += u"Language/%s/" % get_object_or_404(Language, identifier=query)
        else:
            raise Http404
    
    return object_list(
        request, 
        queryset = texts,
        template_name = template_name,
        template_object_name = 'text',
        paginate_by = 25,
        extra_context = extra_context,
    )
