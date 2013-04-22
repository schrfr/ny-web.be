from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.admin import CommentsAdmin

from threadedcomments.models import ThreadedComment


def make_removed(modeladmin, request, queryset):
    queryset.update(is_removed=True)
make_removed.short_description = "Mark selected Threaded comments as removed"


class ThreadedCommentsAdmin(CommentsAdmin):
    fieldsets = (
        (None,
           {'fields': ('content_type', 'object_pk', 'site')}
        ),
        (_('Content'),
           {'fields': ('user', 'user_name', 'user_email', 'user_url', 'title', 'comment')}
        ),
        (_('Hierarchy'),
           {'fields': ('parent',)}
        ),
        (_('Metadata'),
           {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}
        ),
    )
    actions = [make_removed]
    list_per_page = 990
    list_display = ('name', 'title', 'content_type', 'object_pk', 'parent', 'ip_address', 'submit_date', 'is_public', 'is_removed')
    search_fields = ('title', 'comment', 'user__username', 'user_name', 'user_email', 'user_url', 'ip_address')
    raw_id_fields = ("parent",)

admin.site.register(ThreadedComment, ThreadedCommentsAdmin)

