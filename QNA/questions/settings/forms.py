'''
Created on Oct 15, 2014

@author: ejiahug
'''
import os
"""
from string import strip
"""
from django import forms
from questions.settings.base import Setting
from django.utils.translation import ugettext as _
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse

class ImageFormWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        return """
            <img src="%(value)s" /><br />
            %(change)s: <input type="file" name="%(name)s" />
            <input type="hidden" name="%(name)s_old" value="%(value)s" />
            """ % {'name': name, 'value': value, 'change': _('Change this:')}

    def value_from_datadict(self, data, files, name):
        if name in files:
            f = files[name]

            # check file type
            file_name_suffix = os.path.splitext(f.name)[1].lower()

            if not file_name_suffix in ('.jpg', '.jpeg', '.gif', '.png', '.bmp', '.tiff', '.ico'):
                raise Exception('File type not allowed')

            from questions.settings.upload import UPFILES_FOLDER, UPFILES_ALIAS

            storage = FileSystemStorage(str(UPFILES_FOLDER), str(UPFILES_ALIAS))
            new_file_name = storage.save(f.name, f)
            return str(UPFILES_ALIAS) + new_file_name
        else:
            if "%s_old" % name in data:
                return data["%s_old" % name]
            elif name in data:
                return data[name]