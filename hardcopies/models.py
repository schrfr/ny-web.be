from django.db import models
from django.utils.translation import ugettext_lazy as _
from tinymce import models as tinymce_models
from filebrowser.fields import FileBrowseField
from library.models import Text

class Magazine(models.Model):
    """
    Describes a magazine for which print issues can exist
    """
    title      = models.CharField(max_length=50, verbose_name=_('Title'), blank=True)
    identifier = models.SlugField(verbose_name=_('Identifier'), unique=True, help_text=_('Unique identifier. Allows a constant targeting of the issue'))

    def __unicode__(self):
        return u'%s' % self.title

class PrintIssue(models.Model):
    """
    Describes a print issue.
    """
    title      = models.CharField(max_length=50, verbose_name=_('Title'), blank=True)
    number     = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_('Issue Number'))
    pub_date   = models.DateField(verbose_name=_('Publication Date'), help_text=_('Publication date'))
    magazine   = models.ForeignKey(Magazine, verbose_name=_('Magazine'), related_name='magazine')
    cover      = FileBrowseField(max_length=200, directory="covers/", extensions=['.jpg', '.jpeg', '.gif','.png'], 
                                 format='Image')
    identifier = models.SlugField(verbose_name=_('Identifier'), unique=True, help_text=_('Unique identifier. Allows a constant targeting of the issue'))
    summary    = tinymce_models.HTMLField(verbose_name=_('infos'), help_text=_('Enter here your custom text'), blank=True)
    
    def get_absolute_url(self):
        return "/print-issues/%s/%s/" % (self.magazine.identifier, self.identifier)
    
    def __unicode__(self):
        return u'%s %s' % (getattr(self, "name", ""), getattr(self, "number", ""))

class PrintIssueOnlineText(models.Model):
    """
    Describes a text published both in the Print issue and online.
    """
    print_issue = models.ForeignKey(PrintIssue, verbose_name=_('Print Issue'))
    online_text = models.ForeignKey(Text, verbose_name=_('Online Text'), related_name='print_issues')
    order       = models.IntegerField(blank= True, null= True)

    def __unicode__(self):
        return u'%s' % self.print_issue

    class Meta:
        ordering = ('order',)
