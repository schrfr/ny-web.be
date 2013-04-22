from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User

import datetime
import dateutil


class Person(models.Model):
    """
    Describes a Person.
    """
    first_name = models.CharField(_('first name'), blank=True, max_length=100)
    last_name  = models.CharField(_('last name'), blank=True, max_length=100)
    slug       = models.SlugField(_('slug'), unique=True)
    user       = models.ForeignKey(User, blank=True, null=True, help_text=_('If the person is an existing user of your site.'))
    email      = models.EmailField(verbose_name=_('EMail'), blank=True)
    info       = models.TextField(verbose_name=_('infos'), help_text=_('Enter here your custom text'), blank=True)
    
    @property
    def full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)
    
    def __unicode__(self):
        return u'%s' % self.full_name
    
    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')
        db_table = 'people'
        ordering = ('last_name', 'first_name')

