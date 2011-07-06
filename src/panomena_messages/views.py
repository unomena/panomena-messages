from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from panomena_messages.models import Message
from panomena_messages.forms import ComposeForm


@login_required
def inbox(request):
    """View for the inbox of the current user."""
    messages = Message.objects.inbox_for(request.user)
    context = RequestContext(request, {'message_list': messages})
    return render_to_response('messages/inbox.html', context)


@login_required
def outbox(request):
    """View for the outbox of the current user."""
    messages = Message.objects.outbox_for(request.user)
    context = RequestContext(request, {'message_list': messages})
    return render_to_response('messages/outbox.html', context)


@login_required
def compose(request):
    """View for composing a message."""
    context = RequestContext(request)
    if request.method == 'POST':
        form = ComposeForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect('messages_outbox')
    else:
        form = ComposeForm(initial=request.GET)
    context['form'] = form
    return render_to_response('messages/compose.html', context)


@login_required
def delete(request, pk):
    """View for deleting messages."""
    message = get_object_or_404(Message, pk=pk)
    message.delete()
    url = request.GET.get('next')
    if url:
        return redirect(url)
    else:
        return redirect('messages_inbox')
