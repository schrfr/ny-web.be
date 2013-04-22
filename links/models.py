from django.db import models
from django.utils.translation import ugettext_lazy as _


class LinkCategory(models.Model):
    """
    Describes a Link Category.
    Link entries are used to populate the "link" page.
    """
    name       = models.CharField(verbose_name=_('Name'), max_length=50)
    order      = models.IntegerField(verbose_name=_('Order'), blank=True, null=True)
    identifier = models.SlugField(verbose_name=_('Identifier'), unique=True, 
                                  help_text=_('Unique identifier. Allows a constant targeting of the category'))
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name_plural = _('link categories')
        ordering = ('order',)


class Link(models.Model):
    """
    Describes links.
    Link entries are used to populate the "link" page.
    """
    url         = models.URLField(_('url'), unique=True)
    title       = models.CharField(verbose_name=_('Title'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    category    = models.ForeignKey(LinkCategory, verbose_name=_('Category'))
    created     = models.DateTimeField(_('created'), auto_now_add=True)
    modified    = models.DateTimeField(_('modified'), auto_now=True)
    
    def __unicode__(self):
        return self.url
    
    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')
        db_table = "links"
    
    class Admin:
        list_display = ('url', 'description')
        search_fields = ('url', 'description', 'extended')

    