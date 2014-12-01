'''
Created on Oct 28, 2014

@author: ejiahug
'''
from questions.settings.base import Setting, SettingSet
from django.forms.widgets import Textarea, RadioSelect, Select
from django.utils.translation import ugettext_lazy as _

RENDER_CHOICES = (
('markdown', _('Markdown')),
('html', _('HTML')),
('escape', _('Escaped'))
)