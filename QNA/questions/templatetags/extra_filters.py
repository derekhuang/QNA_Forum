'''
Created on Oct 24, 2014

@author: ejiahug
'''

from django import template
from django.utils.safestring import mark_safe
import logging
import markdown

register = template.Library()

@template.defaultfilters.stringfilter
@register.filter
def collapse(input):
    return ' '.join(input.split())


@register.filter
def can_edit_post(user, post):
    return user.can_edit_post(post)


@register.filter
def decorated_int(number, cls="thousand"):
    try:
        number = int(number)    # allow strings or numbers passed in
        if number > 999:
            thousands = float(number) / 1000.0

            if number < 99500:
                format = "%.1f"
            else:
                format = "%.0f"

            s = format % thousands

            return mark_safe("<span class=\"%s\">%sk</span>" % (cls, s))
        return number
    except:
        return number

@register.filter
def or_preview(setting, request):
    if request.user.is_superuser:
        previewing = request.session.get('previewing_settings', {})
        if setting.name in previewing:
            return previewing[setting.name]

    return setting.value

@register.filter
def getval(map, key):
    return map and map.get(key, None) or None


@register.filter
def contained_in(item, container):
    return item in container


@register.filter
def static_content(content, render_mode):
    if render_mode == 'markdown':
        #return mark_safe(markdown.markdown(str(content), ["settingsparser"]))
        return mark_safe(markdown.markdown(str(content)))
    elif render_mode == 'markdown-safe':
        return mark_safe(markdown.markdown(str(content), safe_mode=True))
    elif render_mode == "html":
        return mark_safe(str(content))
    else:
        return str(content)
