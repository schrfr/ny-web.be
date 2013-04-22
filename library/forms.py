# TODO: delete


# from models import *
# from django.forms import ModelForm
# from django.db.models import Q
# 
# class StickyTextForm(ModelForm):
#     def __init__(self,*args,**kwargs):
#         super (StickyTextForm,self ).__init__(*args,**kwargs) # populates the post
#         try:
#             self.instance.zone
#             try:
#                 self.fields['text'].queryset = Text.objects.filter(Q(zone=self.instance.zone) | Q(zone__parent=self.instance.zone))
#             except:
#                 self.fields['text'].queryset = Text.objects.none()
#         except:
#             try:
#                 self.fields['text'].queryset = Text.objects.filter(Q(zone__id=self.data['zone']) | Q(zone__parent__id=self.data['zone']))
#             except:
#                 self.fields['text'].queryset = Text.objects.none()
#     
#     class Meta:
#         model = StickyText

from models import *
from django import forms
from django.db.models import Q

class StickyTextForm(forms.ModelForm):
    """
    StickyText Model Form class.
    """
    def __init__(self,*args,**kwargs):
        super (StickyTextForm,self ).__init__(*args,**kwargs) # populates the post
        try:
            self.instance.zone
            try:
                self.fields['first_text'].queryset = Text.objects.filter(zone=self.instance.zone)
                self.fields['second_text'].queryset = Text.objects.filter(zone=self.instance.zone)
            except:
                self.fields['first_text'].queryset = Text.objects.none()
                self.fields['second_text'].queryset = Text.objects.none()
        except:
            try:
                self.fields['first_text'].queryset = Text.objects.filter(zone__id=self.data['zone'])
                self.fields['second_text'].queryset = Text.objects.filter(zone__id=self.data['zone'])
            except:
                self.fields['first_text'].queryset = Text.objects.none()
                self.fields['second_text'].queryset = Text.objects.none()
    
    class Meta:
        model = StickyText


class TextForm(forms.ModelForm):
    """
    Text Model Form class.
    """
    model = Text
    
    def clean(self):
        cleaned_data = self.cleaned_data
        paragraph_comments = cleaned_data.get("paragraph_comments")
        document_type = cleaned_data.get("document_type")
        
        if paragraph_comments == True and str(document_type) == 'Poetry':
            # raise forms.ValidationError("You may not enable Paragraph comments on a Poetry.\
            # Please desactivate paragraph comments.")
            msg = u"You may not enable Paragraph comments on a Poetry.\
                    Please desactivate paragraph comments or Change the document type."
            self._errors["paragraph_comments"] = ErrorList([msg])
            self._errors["document_type"] = ErrorList([msg])
            
            # These fields are no longer valid. Remove them from the
            # cleaned data.
            del cleaned_data["paragraph_comments"]
            del cleaned_data["document_type"]
        
        return cleaned_data # Always return the full collection of cleaned data.
    
    class Media:
        css = {
            'all': ('/static/css/admin-extra.css',)
        }
        js = (
            '/static/js/jquery-1.3.2.min.js',
            '/static/js/jquery-ui-1.7.2.custom.min.js',
            '/static/js/menu-sort.js',
            '/static/js/delete-paragraphs.js',
        )

