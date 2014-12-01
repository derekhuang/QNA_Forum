'''
Created on Oct 17, 2014

@author: ejiahug
'''
from questions import settings

"""
This is the custom context processor, to convey the context variable (i.e. 'settings') to templates.
It is added to the TEMPLATE_CONTEXT_PROCESSOR in settings.py.  
"""
def application_settings(request):
    return {'settings': settings}