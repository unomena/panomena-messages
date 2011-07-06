from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class MessageManager(models.Manager):

    def inbox_for(self, user):
        """Returns all messages that were received by the given user and are
        not marked as deleted.

        """
        return self.filter(
            recipient=user,
            recipient_deleted__isnull=True,
        )

    def outbox_for(self, user):
        """Returns all messages that were sent by the given user and are not
        marked as deleted.
        """
        return self.filter(
            sender=user,
            sender_deleted__isnull=True,
        )

    def trash_for(self, user):
        """Returns all messages that were either received or sent by the
        given user and are marked as deleted.

        """
        return self.filter(
            recipient=user,
            recipient_deleted__isnull=False,
        ) | self.filter(
            sender=user,
            sender_deleted__isnull=False,
        )


class Message(models.Model):
    """Model for a private message from user to user."""
    subject = models.CharField(_('Subject'), max_length=120)
    body = models.TextField(_('Body'))
    sender = models.ForeignKey(User, related_name='sent_messages',
        verbose_name=_('Sender'))
    recipient = models.ForeignKey(User, related_name='received_messages',
        null=True, blank=True, verbose_name=_('Recipient'))
    parent_message = models.ForeignKey('self', related_name='next_messages',
        null=True, blank=True, verbose_name=_('Parent message'))
    sent = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    read = models.DateTimeField(null=True, blank=True)
    replied = models.DateTimeField(null=True, blank=True)
    sender_deleted = models.DateTimeField(null=True, blank=True)
    recipient_deleted = models.DateTimeField(null=True, blank=True)
    
    objects = MessageManager()
    
    def new(self):
        """Returns whether the recipient has read the message or not."""
        if self.read_at is not None:
            return False
        return True
        
    def replied(self):
        """Returns whether the recipient has written a reply to this message."""
        if self.replied_at is not None:
            return True
        return False
    
    def __unicode__(self):
        return self.subject
    
    @models.permalink
    def get_absolute_url(self):
        return ('messages_detail', [self.id])
    
    class Meta:
        ordering = ['-sent']
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        

def inbox_count_for(user):
    """Returns the number of unread messages for the given user but does
    not mark them seen.

    """
    return Message.objects.filter(
        recipient=user,
        read__isnull=True,
        recipient_deleted__isnull=True,
    ).count()

