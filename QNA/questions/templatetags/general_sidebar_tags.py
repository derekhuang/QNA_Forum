'''
Created on Oct 28, 2014

@author: ejiahug
'''
from django import template
from questions.models import Tag #, Award
from questions.settings.sidebar import * 
from questions.settings import sidebar

from questions.templatetags.extra_filters import static_content

register = template.Library()

@register.inclusion_tag('sidebar/markdown_help.html')
def markdown_help():
    return {}

@register.inclusion_tag('sidebar/recent_awards.html')
def recent_awards():
    #return {'awards': Award.objects.order_by('-awarded_at')[:settings.RECENT_AWARD_SIZE]}
    return {'awards': 0}

@register.inclusion_tag('sidebar/user_blocks.html')
def sidebar_upper():
    if bool(SIDEBAR_UPPER_SHOW.value):
        print(SIDEBAR_LOWER_RENDER_MODE)
   
    return {
        'show': SIDEBAR_UPPER_SHOW.value,
        'content': static_content(SIDEBAR_UPPER_TEXT, 'markdown'),
        'wrap': not SIDEBAR_UPPER_DONT_WRAP.value,
        'blockid': 'sidebar-upper'
    }

@register.inclusion_tag('sidebar/user_blocks.html')
def sidebar_lower():
    return {
        'show': SIDEBAR_LOWER_SHOW.value,
        'content': static_content(SIDEBAR_LOWER_TEXT, 'markdown'),
        'wrap': not SIDEBAR_LOWER_DONT_WRAP.value,
        'blockid': 'sidebar-lower'
    }

@register.inclusion_tag('sidebar/recent_tags.html')
def recent_tags():
    #return {'tags': Tag.active.order_by('-id')[:view.RECENT_TAGS_SIZE]}
    return {'tags': Tag.objects.all()}
    