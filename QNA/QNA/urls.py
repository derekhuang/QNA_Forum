from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.views.generic import RedirectView
import questions.views as app
import os

admin.autodiscover()

APP_PATH = os.path.dirname(__file__)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'QNA.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', app.index, name='index'),
    url(r'^index/$', app.index),
    url(r'^ask/$', app.ask, name='ask'),
    url(r'^search/$', app.ask, name='search'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^%s$' % _('questions/'), app.questions, name='questions'),
    url(r'^feeds/rss[/]?$', app.feed, name='latest_questions_feed'),
    url(r'^%s(?P<tag>.*)/$' % _('tags/'), app.tag, name='tag_questions'),
    url(r'^%s$' % _('tags/'), app.tags, name='tags'),
    url(r'^%s(?P<id>\d+)/(?P<slug>[\w-]*)$' % _('question/'), RedirectView.as_view(url='/questions/%(id)s/%(slug)s')),
    url(r'^%s(?P<id>\d+)/?$' % _('questions/'), app.question, name='question'),
    url(r'^%s(?P<id>\d+)/(?P<slug>.*)$' % _('questions/'), app.question, name='question'),
    
    (r'^i18n/', include('django.conf.urls.i18n')),
)
