# *-* encoding: utf-8 *-*

from datetime import date
from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from people.models import Person
from tinymce import models as tinymce_models
from BeautifulSoup import BeautifulSoup


class Zone(models.Model):
    """
    Describes a zone
    """
    name       = models.CharField(verbose_name=_('Name'), max_length=100)
    identifier = models.SlugField(verbose_name=_('Identifier'), unique=True, 
                                  help_text=_('Unique identifier. Allows a constant targeting of the publisher'))
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        ordering = ('name',)

class Language(models.Model):
    """
    Describes a language
    """
    name       = models.CharField(verbose_name=_('Name'), max_length=100)
    identifier = models.SlugField(verbose_name=_('Identifier'), unique=True, 
                                  help_text=_('Unique identifier. Allows a constant targeting of the language'))
    
    def __unicode__(self):
        return u'%s' % self.name

class Keyword(models.Model):
    """
    Describes a Tag.
    """
    name = models.CharField(max_length=50, verbose_name=_('Tag Name'))
    identifier = models.SlugField(verbose_name=_('Identifier'), unique=True, 
                                  help_text=_('Unique identifier. Allows a constant targeting of the language'))
    
    def get_absolute_url(self):
        return "/web-archive/tag/%s/" % self.identifier
    
    def __unicode__(self):
        return u'%s' % self.name

class DocumentType(models.Model):
    """
    Describes a Document Type, for instance a "Poetry", "Essay" and so on.
    """
    name       = models.CharField(max_length=50, verbose_name=_('Type Name'))
    identifier = models.SlugField(verbose_name=_('Identifier'), unique=True, help_text=_('Unique identifier. Allows a constant targeting of the document'))
    
    def __unicode__(self):
        return u'%s' % self.name

class Text(models.Model):
    """
    Describes a text document.
    """
    title               = models.CharField(max_length=200, verbose_name=_('Title'), help_text=_('Document main title'))
    authors             = models.ManyToManyField(Person, verbose_name=_('Authors'), related_name='authors_set', null=True, blank=True,
                                                 help_text=_('Name of the person, the organisation or the department who created the document'))
    keywords            = models.ManyToManyField(Keyword, verbose_name=_('Keywords/Tags'), null=True, blank=True,)
    description         = models.CharField(max_length=500, verbose_name=_('Description'), 
                                           help_text=_('Abstract. Limited to 500 characters'), blank=True)
    pub_date            = models.DateField(verbose_name=_('Publication Date'), help_text=_('Publication date'))
    modif_date          = models.DateField(verbose_name=_('Modification Date'), help_text=_('Modification date'), null=True, blank=True,)
    identifier          = models.SlugField(verbose_name=_('Identifier'), unique=True, help_text=_('Unique identifier. Allows a constant targeting of the document'))
    language            = models.ForeignKey(Language, verbose_name=_('Language'))
    document_type       = models.ForeignKey(DocumentType, verbose_name=_('Document Type'))
    general_comments    = models.BooleanField(verbose_name=_('Allow general comments?'))
    paragraph_comments  = models.BooleanField(verbose_name=_('Allow paragraph comments?'))
    publish             = models.BooleanField(verbose_name=_('Publish?'), default=True)
    highlight           = models.BooleanField(verbose_name=_('Highlight?'), default=True)
    zone                = models.ForeignKey(Zone, verbose_name=_('Publish under'), help_text=_('Select the zone where the text should appear'))
    body                = tinymce_models.HTMLField(verbose_name=_('Body'), 
                                        help_text=_('<div id="paragraphs_warning">Modifying a text might delete its current paragraph comments, if any!</div>'))
    
    def future(self):
        return self.pub_date > date.today()
    
    @property
    def has_paragraphs(self):
        if self.paragraph_set.all() is None:
            return False
        else:
            return True
    
    # use ", ".join instead
    @property
    def all_authors(self):
        authors = u''
        for author in self.authors.all():
            authors += u'%s, ' % author.full_name
        return u'%s' % authors
    
    @property
    def all_keywords(self):
        keywords = ''
        for keyword in self.keywords.all():
            keywords += u'%s, ' % keyword.name
        return u'%s' % keywords
    
    @property
    def all_general_comments(self):
        """Return all comment objects for the instance."""
        ctt = ContentType.objects.get(app_label="library", model="text")
        return Comment.objects.filter(Q(content_type=ctt), Q(object_pk=self.id))
    
    @property
    def all_paragraph_comments(self):
        """Return all comment objects for the instance."""
        ctp = ContentType.objects.get(app_label="library", model="paragraph")
        return Comment.objects.filter(Q(content_type=ctp)).objects.filter(Q(text=self.id))
    
    def get_absolute_url(self):
        return u"/%s/%s.html" % (self.zone.identifier, self.identifier)

    def save(self):        
        super(Text, self).save()
        if self.paragraph_comments == True:
            paragraphs = Paragraph.objects.filter(text=self)
            for paragraph in paragraphs:
                paragraph.delete()
            # import re
            # import markdown
            # output = markdown.markdown(self.body) 
            # p = re.compile(r'<p>(.*?)</p>', re.S)
            # for l in p.findall(output):
            #     if not l.isspace():
            #         print l.encode('utf-8')
            #         paragraph = Paragraph()
            #         paragraph.text = self
            #         paragraph.content = l.encode('utf-8')
            #         paragraph.save()
            soup = BeautifulSoup(self.body)
            for p in soup:
                if str(p).isspace():
                    pass
                elif str(p) == "<p>&nbsp;</p>":
                    pass
                else:
                    paragraph = Paragraph()
                    paragraph.text = self
                    paragraph.content = unicode(p).encode('utf-8')
                    paragraph.save()
    
    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        ordering = ('-pub_date',)

class Paragraph(models.Model):
    """
    Describes a paragraph to comment on. Automatically created 
    after a Text when the paragraph comment option is checked.
    """
    text    = models.ForeignKey(Text)
    content = models.TextField()
    
    def __unicode__(self):
        return u'%s' % self.content[0:100]
    
    def get_absolute_url(self):
        return u"%s#paragraph_%s" % (self.text.get_absolute_url(), self.id)

class RelatedText(models.Model):
    """
    Describes a related text inside the nY website.
    """
    from_text = models.ForeignKey(Text, verbose_name=_('Text'), related_name='related_texts')
    to_text   = models.ForeignKey(Text, verbose_name=_('Linked Text'), related_name='from_texts')
    order     = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return u'%s' % self.to_text
    
    class Meta:
        ordering = ('order',)

class StickyText(models.Model):
    """
    Allows one to pick up the selected text for each zone
    """
    
    zone = models.ForeignKey(Zone, unique=True, verbose_name=_('Zone'), 
                             help_text=_('If you are creating a new Higlighted Text Object, click \'Save and continue editing\' button to populate \'First Text\' and \'Second Text\' fields'))
    first_text = models.ForeignKey(Text, verbose_name=_('First Text'), null=True, blank=True, related_name='first_highlights')
    second_text = models.ForeignKey(Text, verbose_name=_('Second Text'), related_name='second_highlights', null=True, blank=True)
    
    def __unicode__(self):
        return u'%s, %s, %s' % (self.zone, self.first_text, self.second_text)
    
    class Meta:
        pass
