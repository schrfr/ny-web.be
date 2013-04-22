from django.contrib import admin
from django import forms
from django.forms.util import ErrorList
from library.models import *
from library.forms import *


class ZoneAdmin(admin.ModelAdmin):
    """
    Zone Model Admin class.
    """
    prepopulated_fields = {"identifier": ("name",)}

admin.site.register(Zone, ZoneAdmin)


class LanguageAdmin(admin.ModelAdmin):
    """
    Language Model Admin class.
    """
    prepopulated_fields = {"identifier": ("name",)}

admin.site.register(Language, LanguageAdmin)


class RelatedTextInline(admin.StackedInline):
    """
    RelatedText Model Inline Admin class.
    """
    model   = RelatedText
    fk_name = "from_text"
    extra   = 3


class ParagraphInline(admin.StackedInline):
    """
    Paragraph Model Inline Admin class.
    """
    model = Paragraph
    extra = 0


# TODO: delete
class ParagraphAdmin(admin.ModelAdmin):
    """
    Paragraph Model Admin class.
    """
    pass

admin.site.register(Paragraph, ParagraphAdmin)


class KeywordAdmin(admin.ModelAdmin):
    """
    Keyword Model Admin class.
    """
    prepopulated_fields = {"identifier": ("name",)}

admin.site.register(Keyword, KeywordAdmin)


class DocumentTypeAdmin(admin.ModelAdmin):
    """
    DocumentType Model Admin class.
    """
    prepopulated_fields = {"identifier": ("name",)}

admin.site.register(DocumentType, DocumentTypeAdmin)


class TextAdmin(admin.ModelAdmin):
    """
    Text Model Admin class.
    """
    list_display = ('title', 'all_authors', 'zone', 'all_keywords', 'pub_date', 'highlight')
    list_filter = ('zone', 'pub_date', 'highlight')
    inlines = [RelatedTextInline,]
    filter_horizontal = ['keywords', 'authors']
    prepopulated_fields = {"identifier": ("title",)}
    fieldsets = (
        (None, {
            'fields': (('title', 'identifier'),),
        }),
        ('Zone and comments', {
            'fields': (('publish', 'zone'), 'highlight', ('general_comments', 'paragraph_comments')),
        }),
        ('Content', {
            'fields': ('description', 'body',),
        }),
        ('Metadata', {
            'fields': (('pub_date', 'modif_date'), 'authors', 'keywords', 'document_type', 'language'),
        }),
    )
    
    def formfield_for_dbfield(self, db_field, **kwargs):
            formfield = super(TextAdmin, self).formfield_for_dbfield(db_field, **kwargs)
            
            if db_field.name == 'description':
                formfield.widget = forms.Textarea()
                formfield.widget.attrs['class'] = 'vLargeTextField ' + formfield.widget.attrs.get('class', '')
            
            return formfield

admin.site.register(Text, TextAdmin, form=TextForm)


class StickyTextAdmin(admin.ModelAdmin):
    """
    StickyText Model Admin class.
    """
    list_display = ('zone', 'first_text', 'second_text')

admin.site.register(StickyText, StickyTextAdmin, form=StickyTextForm,)
