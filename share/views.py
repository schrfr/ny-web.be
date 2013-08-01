# TODO: only what is necessary 
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
# TODO: use requestcontext instead
from django.conf import settings 

from library.models import Text
from forms import ShareForm


def share(request, slug):
    """
    Share view.
    Allows readers to send a link to a text by Email.
    """
    text = Text.objects.get(identifier=slug)
    
    if request.method == 'POST': # If the form has been submitted...
        form = ShareForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            name      = form.cleaned_data['name']
            sender    = form.cleaned_data['sender']
            to        = form.cleaned_data['to']
            cc_myself = form.cleaned_data['cc_myself']
            
            recipients = [to]
            if cc_myself:
                recipients.append(sender)
            
            subject = u"%s wants to share a text with you from nY" % name
            
            message = u"""
                %s would like to share with you the following text:
            """ % (name)
            
            #from django.core.mail import send_mail
            from django.core.mail import EmailMultiAlternatives
            #send_mail(subject, message, sender, recipients)
            html_content = u'''
                <a style='font-family: "American Typewriter", "Courier New"; font-weight: bold; color: black; font-size: 11em; line-height:0.8em; text-decoration: none;' href='http://test.ny-web.be/'>nY</a>
                <div style="font-family: Georgia; margin-top: 8px; margin-bottom: 20px; width:500px;">
                    <span style="font-weight: bold;">website en tijdschrift voor literatuur, kritiek &amp; amusement, <br />
                    voorheen</span> <span style="font-style: italic;">yang &amp; freespace Nieuwzuid</span>                                
                </div>
                
                <p style="font-family: Georgia; font-size: 14px;">%s would like to share with you the following text: <a href="%s">%s</a>.</p>
            ''' % (name, 'http://test.ny-web.be' + text.get_absolute_url(), text)

            msg = EmailMultiAlternatives(subject, message, sender, recipients)
            msg.attach_alternative(html_content, "text/html")
            msg.content_subtype = "html"
            msg.send()
            
            back2text = """
                        <p><a href='%s'>Return to the text.</a></p>
                        """ % text.get_absolute_url()
            
            return HttpResponse(html_content + back2text )
            # return HttpResponseRedirect('/share/thanks/') # Redirect after POST
    else:
        form = ShareForm() # An unbound form

    return render_to_response('share/share.html', {
        'form': form,
        'text': text,
        'MEDIA_URL': settings.MEDIA_URL,
    }, context_instance=RequestContext(request))

