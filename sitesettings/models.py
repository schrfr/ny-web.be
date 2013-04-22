from django.db import models
from django.utils.translation import ugettext_lazy as _


class SiteSettings(models.Model):
    
    site = models.OneToOneField('sites.Site', unique=True, related_name='site_settings')

    url_big_banner           = models.URLField(_('Big Banner Link'), blank=True ,)
    show_big_banner          = models.BooleanField(verbose_name=_('Display the big banner?'))
    big_banner               = models.ImageField(upload_to="banners/big", blank=True, 
                                                 help_text='The big banner should be exactly sized 1000x90 px')
    
    url_first_small_banner   = models.URLField(_('First Small Banner Link'), blank=True,)
    show_first_small_banner  = models.BooleanField(verbose_name=_('Display the small banner?'))
    first_small_banner       = models.ImageField(upload_to="banners/small", blank=True, 
                                               help_text='The small banner should be exactly sized 226x226 px')
    
    url_second_small_banner  = models.URLField(_('Second Small Banner Link'), blank=True)
    show_second_small_banner = models.BooleanField(verbose_name=_('Display the small banner?'))
    second_small_banner      = models.ImageField(upload_to="banners/small", blank=True, 
                                             help_text='The small banner should be exactly sized 226x226 px')
    
    
    def __unicode__(self):
        return u"%s" % self.site
    
    class Meta:
        verbose_name = _('Site Banner')
        verbose_name_plural = _('Site Banners')
    