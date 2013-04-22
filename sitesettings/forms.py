from django import forms
from models import SiteSettings
from django.core.files.images import get_image_dimensions

class SiteSettingsForm(forms.ModelForm):
    """
    SiteSettings Model Form class.
    """
    model = SiteSettings
    
    def clean_big_banner(self):
        if self.cleaned_data['big_banner']:
            w, h = get_image_dimensions(self.cleaned_data['big_banner'])
            if w != 1000 or h != 90:
                raise forms.ValidationError("Your image is %sx%s. It should be 1000x90" % (w, h))
        return self.cleaned_data['big_banner']        
    
    def clean_first_small_banner(self):
        if self.cleaned_data['first_small_banner']:
            w, h = get_image_dimensions(self.cleaned_data['first_small_banner'])
            if w != 226 or h != 226:
                raise forms.ValidationError("Your image is %sx%s. It should be 226x226" % (w, h))
        return self.cleaned_data['first_small_banner']

    def clean_second_small_banner(self):
        if self.cleaned_data['second_small_banner']:
            w, h = get_image_dimensions(self.cleaned_data['second_small_banner'])
            if w != 226 or h != 226:
                raise forms.ValidationError("Your image is %sx%s. It should be 226x226" % (w, h))
        return self.cleaned_data['second_small_banner']
