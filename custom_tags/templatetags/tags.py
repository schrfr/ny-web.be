from django.template import Library, Node, TemplateSyntaxError
from library.models import Keyword, DocumentType, Language
from people.models import Person

register = Library()

class set_context_variable(Node):
    def __init__(self, varname, objects):
        self.varname = varname
        self.objects = objects
    
    def render(self, context):        
        # tags = Keyword.objects.all().order_by('name')
        context[self.varname] = self.objects
        return ''

def get_all_tags(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "get_all_tags tag takes exactly 2 arguments"
    if bits[1] != 'as':
        raise TemplateSyntaxError, "fisrt argument to get_all_tags tag must be 'as'"
    return set_context_variable(
        bits[2], 
        Keyword.objects.all().order_by('name')
    )

get_all_tags = register.tag(get_all_tags)

def get_all_authors(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "get_all_authors tag takes exactly 2 arguments"
    if bits[1] != 'as':
        raise TemplateSyntaxError, "fisrt argument to get_all_tags tag must be 'as'"
    return set_context_variable(
        bits[2], 
        Person.objects.filter(authors_set__isnull=False).distinct().order_by('last_name')
    )

get_all_authors = register.tag(get_all_authors)

def get_all_types(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "get_all_types tag takes exactly 2 arguments"
    if bits[1] != 'as':
        raise TemplateSyntaxError, "fisrt argument to get_all_types tag must be 'as'"
    return set_context_variable(
        bits[2], 
        DocumentType.objects.all().order_by('name')
    )

get_all_types = register.tag(get_all_types)


def get_all_languages(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "get_all_languages tag takes exactly 2 arguments"
    if bits[1] != 'as':
        raise TemplateSyntaxError, "fisrt argument to get_all_languages tag must be 'as'"
    return set_context_variable(
        bits[2], 
        Language.objects.all().order_by('name')
    )

get_all_languages = register.tag(get_all_languages)


def tag_list(context, zone):
    objects = Keyword.objects.filter(text__zone=zone).distinct().order_by('name')
    return {'tags': objects, 'zone': context['zone']}

register.inclusion_tag('side-menu.html', takes_context=True)(tag_list)

def author_list(context, zone):
    objects = Person.objects.filter(authors_set__zone=zone).distinct().order_by('last_name')
    return {'authors': objects, 'zone': context['zone']}

register.inclusion_tag('side-menu.html', takes_context=True)(author_list)

def type_list(context, zone):
    objects = DocumentType.objects.filter(text__zone=zone).distinct().order_by('name')
    return {'types': objects, 'zone': context['zone']}

register.inclusion_tag('side-menu.html', takes_context=True)(type_list)

def language_list(context, zone):
    objects = Language.objects.filter(text__zone=zone).distinct().order_by('name')
    return {'languages': objects, 'zone': context['zone']}

register.inclusion_tag('side-menu.html', takes_context=True)(language_list)
