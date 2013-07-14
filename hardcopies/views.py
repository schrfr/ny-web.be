from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from hardcopies.models import PrintIssue, Magazine
from library.models import Text

def hard_copy(request, issue_slug, magazine_slug='ny'):
    """
    Hard Copy view.
    Retrieves:
    * the issue matching the provided issue_slug,
    * the rest of the issues.
    * the texts published online
    """
    current_issue = get_object_or_404(PrintIssue, identifier=issue_slug)
    magazine = get_object_or_404(Magazine, identifier=magazine_slug)
    other_issues  = PrintIssue.objects.order_by('-pub_date').filter(magazine__identifier=magazine_slug)
    online_texts  = Text.objects.filter(print_issues__print_issue__identifier=issue_slug).order_by('-pub_date')
    
    my_dict = {
        'current_issue' : current_issue, 
        'other_issues'  : other_issues, 
        'online_texts'  : online_texts,
        'magazine'      : magazine,
    }
    
    return render_to_response('hard-copy.html', my_dict, context_instance=RequestContext(request))

def archive_redirect(request, slug='ny'):
    try:
        # it could be /print-issues/{ny|freespace-nieuwzuid|yang}/
        # we want to redirect to the latest issue
        magazine = Magazine.objects.get(identifier=slug)
    except Magazine.DoesNotExist:
        # it could be an ald ny url of the form /print-issues/apr-2013-17/
        # we want to redirect to /print-issues/ny/apr-2013-17/
        current_issue = get_object_or_404(PrintIssue, identifier=slug)
        url = current_issue.get_absolute_url()
        return redirect(url, permanent=True)
        
    last_issue = PrintIssue.objects.order_by('-pub_date').filter(magazine__identifier=slug)[0]
    url = last_issue.get_absolute_url()
    return redirect(url)
