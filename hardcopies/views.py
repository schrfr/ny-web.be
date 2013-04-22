from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from hardcopies.models import PrintIssue
from library.models import Text


def hard_copy(request, slug):
    """
    Hard Copy view.
    Retrieves:
    * the issue matching the provided slug,
    * the rest of the issues.
    * the texts published online
    """
    current_issue = get_object_or_404(PrintIssue, identifier=slug)
    other_issues  = PrintIssue.objects.order_by('-pub_date')
    online_texts  = Text.objects.filter(print_issues__print_issue__identifier=slug).order_by('-pub_date')
    
    my_dict = {
        'current_issue' : current_issue, 
        'other_issues'  : other_issues, 
        'online_texts'  : online_texts,
    }
    
    return render_to_response('hard-copy.html', my_dict, context_instance=RequestContext(request))
