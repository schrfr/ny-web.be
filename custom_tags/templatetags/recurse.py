from django import template
from django.template import Node
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.template.defaultfilters import stringfilter
import operator

register = template.Library()

# The first argument *must* be called "context" here.
def recurse(context, comment):
    """
    recursive
    """
    return {
        'view'          : context['view'],
        'cc'            : context['cc'],
        'cp'            : context['cp'],
        'parent_comment': comment,
        'user'          : context['user']
    }
# Register the custom tag as an inclusion tag with takes_context=True.
register.inclusion_tag('comment.html', takes_context=True)(recurse)


@stringfilter
def to_int(value):
    return int(value)
    
register.filter('to_int', to_int)


class recurse_all_comments(Node):
    def __init__(self, bla, varname):
        self.varname = varname
        self.obj = template.Variable(bla)
        self.results = []
    
    def recurse_comments(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        qs = Comment.objects.filter(content_type=ct, object_pk=obj.pk)
        for comment in qs:
            self.results.append(comment)
            self.recurse_comments(comment)
    
    def render(self, context):
        
        item = self.obj.resolve(context)
        
        self.recurse_comments(item)
        for p in item.paragraph_set.all():
            self.recurse_comments(p)
        
        context[self.varname] = sorted(self.results, key=operator.attrgetter('id')) 
        self.results = []
        return ''


def get_all_comments(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError, "get_all_comments tag takes exactly four arguments"
    if bits[1] != 'for':
        raise template.TemplateSyntaxError, "third argument to get_all_comments tag must be 'for'"
    if bits[3] != 'as':
        raise template.TemplateSyntaxError, "third argument to get_all_comments tag must be 'as'"
    return recurse_all_comments(bits[2], bits[4])
get_all_comments = register.tag(get_all_comments)


def head(value,arg):
    if len(value) >= arg:
        print "head"
        return value[:arg]
    else:
        return value
register.filter('head', head)


def isgreater(value,arg):
    if value >= arg:
        return True
    else:
        return False
register.filter('isgreater', isgreater)
