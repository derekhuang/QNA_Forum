from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext as _
from django.contrib import admin
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
)
