from django import forms


class ShareForm(forms.Form):
    """
    Share Model Form class.
    """
    name      = forms.CharField(max_length=100, label="name")
    sender    = forms.EmailField(label="Your email address")
    to        = forms.EmailField(label="Your friend's email address")
    cc_myself = forms.BooleanField(required=False, label="I'd like to receive a copy")

