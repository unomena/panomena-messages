from django import forms
from django.utils.translation import ugettext_lazy as _

from panomena_messages.fields import CommaSeparatedUserField
from panomena_messages.models import Message


class ComposeForm(forms.Form):
    pass

    recipient = CommaSeparatedUserField(
        label=_(u'Recipient'),
    )
    subject = forms.CharField(
        label=_(u'Subject'),
    )
    body = forms.CharField(
        label=_(u'Body'),
        widget=forms.Textarea(),
    )
    parent_message_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
    )

    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(ComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter
                
    def save(self, sender):
        """Uses field values to fill a message object and saves it."""
        data = self.cleaned_data
        recipients = data['recipient']
        subject = data['subject']
        body = data['body']
        parent_message_id = data.get('parent_message_id')
        # send a message to every recipient in the list
        messages = []
        for recipient in recipients:
            message = Message.objects.create(
                sender=sender,
                recipient=recipient,
                subject=subject,
                body=body,
                parent_message_id=parent_message_id,
            )
            messages.append(message)
        # return the create messages
        return messages
