from django import forms
from threadedcomments.forms import ThreadedCommentForm as CommentForm
from captcha.fields import CaptchaField


class ThreadedCommentForm(CommentForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(ThreadedCommentForm, self).__init__(*args, **kwargs)
        self.fields.pop('title')
        self.fields['honeypot'].widget = forms.HiddenInput()
