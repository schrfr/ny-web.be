from django.template import Library
import re
from datetime import datetime
import time
from django import template


register = Library()

@register.filter
def in_list(value,arg):
    return value in arg

def wrapimages(value, arg=None):
    p = re.compile(r'(<img.*?/>)', re.S)
    if arg is not None:
        r = r'<div class="%s">\1</div>' % arg
    else:
        r = r'<div>\1</div>'
    return p.sub(r, value)
register.filter('wrapimages', wrapimages)
wrapimages.is_safe = True



class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''

def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.
    
    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}
        
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)

register.tag('assign', do_assign)

@register.filter
def todatetime(value):
    return datetime(*time.localtime(time.mktime(value))[:6])

