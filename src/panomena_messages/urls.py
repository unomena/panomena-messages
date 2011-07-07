from django.conf.urls.defaults import *


urlpatterns = patterns('panomena_messages.views',
    url(r'^inbox/$', 'inbox', {}, 'messages_inbox'),
    url(r'^outbox/$', 'outbox', {}, 'messages_outbox'),
    url(r'^compose/$', 'compose', {}, 'messages_compose'),
    url(r'^(?P<pk>\d+)/delete/$', 'delete', {}, 'messages_delete'),
)
