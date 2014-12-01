'''
Created on Oct 15, 2014

@author: ejiahug
'''
from questions.models import AnonymousUser

class ObjectBase(object):
    class Argument(object):
        def __init__(self, argument):
            self.argument = argument

        def __call__(self, context):
            if callable(self.argument):
                user = context.get('request', None) and context['request'].user or AnonymousUser()
                return self.argument(user, context)
            else:
                return self.argument

    def __init__(self, visibility=None, weight=500, name=''):
        self.visibility = visibility
        self.weight = weight
        self.name = name

    def _visible_to(self, user):
        return (not self.visibility) or (self.visibility and self.visibility.show_to(user))

    def can_render(self, context):
        try:
            return self._visible_to(context['request'].user)
        except KeyError:
            try:
                return self._visible_to(context['viewer'])
            except KeyError:
                return self._visible_to(AnonymousUser())

    def render(self, context):
        return ''

class LoopBase(ObjectBase):
    def update_context(self, context):
        pass
    
class PageTab(LoopBase):
    def __init__(self, tab_name, tab_title, url_getter, weight, name=''):
        super(PageTab, self).__init__(weight=weight, name=name)
        self.tab_name = tab_name
        self.tab_title = tab_title
        self.url_getter = url_getter

    def update_context(self, context):
        context.update(dict(
            tab_name=self.tab_name,
            tab_title=self.tab_title,
            tab_url=self.url_getter()
        ))
