'''
Created on Oct 13, 2014

@author: ejiahug
'''
import re
import os
import logging
import math
from django import template
from django.utils.encoding import smart_text, force_text, smart_str
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from questions.utils import html
from questions import settings
from questions.settings import view

register = template.Library()

@register.simple_tag
def media(url):
    """
    url = skins.find_media_source(url)
    """
    if url:
        # Create the URL prefix.
        """
        url_prefix = settings.FORCE_SCRIPT_NAME + '/m/'
        """
        url_prefix = 'http://127.0.0.1:8000' + '/m/'

        # Make sure any duplicate forward slashes are replaced with a single
        # forward slash.
        url_prefix = re.sub("/+", "/", url_prefix)

        url = url_prefix + url
        return url
    
class DeclareNode(template.Node):
    dec_re = re.compile('^\s*(\w+)\s*(:?=)\s*(.*)$')

    def __init__(self, block):
        self.block = block

    def render(self, context):
        source = self.block.render(context)

        for line in source.splitlines():
            m = self.dec_re.search(line)
            if m:
                clist = list(context)
                clist.reverse()
                d = {}
                d['_'] = _
                d['os'] = os
                d['html'] = html
                d['reverse'] = reverse
                d['settings'] = settings
                d['smart_str'] = smart_str
                d['smart_unicode'] = smart_text
                d['force_unicode'] = force_text
                for c in clist:
                    d.update(c)
                try:
                    command = m.group(3).strip()
                    context[m.group(1).strip()] = eval(command, d)
                except Exception as e:
                    logging.error("Error in declare tag, when evaluating: %s" % m.group(3).strip())
        return ''

@register.tag(name='declare')
def do_declare(parser, token):
    nodelist = parser.parse(('enddeclare',))
    parser.delete_first_token()
    return DeclareNode(nodelist)

@register.simple_tag
def get_tag_font_size(tag):
    return 10
    """
    occurrences_of_current_tag = tag.used_count

    # Occurrences count settings
    min_occurs = int(view.TAGS_CLOUD_MIN_OCCURS)
    max_occurs = int(view.TAGS_CLOUD_MAX_OCCURS)

    # Font size settings
    min_font_size = int(view.TAGS_CLOUD_MIN_FONT_SIZE)
    max_font_size = int(view.TAGS_CLOUD_MAX_FONT_SIZE)

    # Calculate the font size of the tag according to the occurrences count
    weight = (math.log(occurrences_of_current_tag)-math.log(min_occurs))/(math.log(max_occurs)-math.log(min_occurs))
    font_size_of_current_tag = min_font_size + int(math.floor((max_font_size-min_font_size)*weight))

    return font_size_of_current_tag
    """