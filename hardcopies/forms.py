from django import forms
from models import Text


class PrintIssueForm(forms.ModelForm):
    """
    PrintIssue Model Form class.
    """
    model = Text
    
    class Media:
        css = {
            'all': ('/static/css/admin-extra.css',)
        }
        js = (
            '/static/js/jquery-1.3.2.min.js',
            '/static/js/jquery-ui-1.7.2.custom.min.js   ',
            '/static/js/menu-sort.js',
        )
