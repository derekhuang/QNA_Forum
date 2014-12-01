'''
Created on Oct 24, 2014

@author: ejiahug
'''
from django import template
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
#from forum.models import Tag, MarkedTag
from questions.templatetags import argument_parser
from questions import settings

register = template.Library()

class QuestionItemNode(template.Node):
    template = template.loader.get_template('question_item.html')

    def __init__(self, question, options):
        self.question = template.Variable(question)
        self.options = options

    def render(self, context):
        return self.template.render(template.Context({
            'question': self.question.resolve(context),
            'question_summary': self.options.get('question_summary', 'no' ) == 'yes',
            'favorite_count': self.options.get('favorite_count', 'no') == 'yes',
            'signature_type': self.options.get('signature_type', 'lite'),
        }))
        
@register.tag
def question_list_item(parser, token):
    tokens = token.split_contents()[1:]
    return QuestionItemNode(tokens[0], argument_parser(tokens[1:]))

"""
@register.inclusion_tag('question_list/tag_selector.html', takes_context=True)
def tag_selector(context):
    request = context['request']
    show_interesting_tags = settings.SHOW_INTERESTING_TAGS_BOX

    if request.user.is_authenticated():
        pt = MarkedTag.objects.filter(user=request.user)
        return {
            'request' : request,
            "interesting_tag_names": pt.filter(reason='good').values_list('tag__name', flat=True),
            'ignored_tag_names': pt.filter(reason='bad').values_list('tag__name', flat=True),
            'user_authenticated': True,
            'show_interesting_tags' : show_interesting_tags,
        }
    else:
        return { 'request' : request, 'user_authenticated': False, 'show_interesting_tags' : show_interesting_tags }
"""