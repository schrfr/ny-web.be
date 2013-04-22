from django.contrib import admin
from hardcopies.models import PrintIssue, PrintIssueOnlineText
from hardcopies.forms import PrintIssueForm


class PrintIssueOnlineTextInline(admin.StackedInline):
    """
    PrintIssueOnlineText Model Inline Admin class.
    """
    model = PrintIssueOnlineText
    extra = 6


class PrintIssueAdmin(admin.ModelAdmin):
    """
    PrintIssue Model Admin class.
    """
    list_display = ('title', 'number')
    prepopulated_fields = {"identifier": ("title", "number")}
    inlines = [PrintIssueOnlineTextInline,]
    fieldsets = (
        (None, {
            'fields': (('title', 'number'), 'identifier', 'pub_date', 'cover', 'summary'),
        }),
    )
    

admin.site.register(PrintIssue, PrintIssueAdmin, form=PrintIssueForm)
