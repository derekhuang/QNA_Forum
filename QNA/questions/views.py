#coding:utf-8
from django.shortcuts import render, render_to_response
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.views.static import serve
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.db.models import Q, Count

from questions import settings
from questions.utils import pagination
from questions.utils.pagination import generate_uri
from questions.models import Question, Tag, Answer, Comment
from questions.settings import ONLINE_USERS
from questions.modules import ui, ui_objects
from questions.modules.decorators import *
from questions.settings.view import * 
import os
import datetime


class HottestQuestionsSort(pagination.SortBase):
    def apply(self, questions):
        return questions.extra(select={'new_child_count': '''
            SELECT COUNT(1)
                FROM forum_node fn1
                WHERE fn1.abs_parent_id = forum_node.id
                    AND fn1.id != forum_node.id
                    AND NOT(fn1.state_string LIKE '%%(deleted)%%')
                    AND added_at > %s'''
            },
            select_params=[ (datetime.datetime.now() - datetime.timedelta(days=2))
                .strftime('%Y-%m-%d')]
        ).order_by('-new_child_count', 'last_activity_at')

class UnansweredQuestionsSort(pagination.SortBase):
    def apply(self, questions):
        return questions.extra(select={'answer_count': '''
            SELECT COUNT(1)
                FROM forum_node fn1
                WHERE fn1.abs_parent_id = forum_node.id
                    AND fn1.id != forum_node.id
                    AND fn1.node_type='answer'
                    AND NOT(fn1.state_string LIKE '%%(deleted)%%')'''
            }).order_by('answer_count', 'last_activity_at')

class QuestionListPaginatorContext(pagination.PaginatorContext):
    def __init__(self, id='QUESTIONS_LIST', prefix='', pagesizes=(15, 30, 50), default_pagesize=30):
        super (QuestionListPaginatorContext, self).__init__(id, sort_methods=(
            #(_('active'), pagination.SimpleSort(_('active'), '-last_activity_at', _("Most <strong>recently updated</strong> questions"))),
            (_('newest'), pagination.SimpleSort(_('newest'), '-published_time', _("most <strong>recently asked</strong> questions"))),
            #(_('hottest'), HottestQuestionsSort(_('hottest'), _("most <strong>active</strong> questions in the last 24 hours</strong>"))),
            (_('mostlike'), pagination.SimpleSort(_('most like'), '-like', _("most <strong>LIKE</strong> questions"))),
            #(_('unanswered'), UnansweredQuestionsSort('unanswered', "questions with no answers")),
        ), pagesizes=(15, 30, 50), default_pagesize=default_pagesize, prefix=prefix)

# Create your views here.
"""
This is the decorator function to render the template with custom context processor.
"""
def render(template=None, tab=None, tab_title='', weight=500, tabbed=True):
    def decorator(func):        
        def decorated(context, request, *args, **kwargs):
            if request.user.is_authenticated():
                pass
                #ONLINE_USERS[request.user] = datetime.datetime.now()

            if isinstance(context, HttpResponse):
                return context

            if tab is not None:
                context['tab'] = tab

            return render_to_response(context.pop('template', template), context,
                                      context_instance=RequestContext(request))

        if tabbed and tab and tab_title:
            ui.register(ui.PAGE_TOP_TABS,
                        ui.PageTab(tab, tab_title, lambda: reverse(func.__name__), weight=weight))
        """
        The effect of the following line of code is equal to call func(), but with some more decorated functionalities
        which is defined in modules/decorator.py. 
        Actually decorate.result.withfn(decorated, needs_params=Ture)() is another decorator. Totally there are 2 decorators.
        """    
        return decorate.result.withfn(decorated, needs_params=True)(func)

    return decorator

@render('index.html')
def index(request):
    paginator_context = QuestionListPaginatorContext()
    paginator_context.base_path = reverse('questions')
    return question_list(request,
                         Question.objects.all(),
                         base_path=reverse('questions'),
                         feed_url=reverse('latest_questions_feed'),
                         paginator_context=paginator_context)

def questions(request):
    pass

def feed(request):
    pass

def tag(request, tag):
    pass

def tags(request):
    pass
    
def question(request):
    pass

"""
def index(request):
    posts = Question.objects.all()
    template_name = loader.get_template("index.html")
    c = Context({ 'posts': posts})
    return render_to_response("index.html", c, context_instance=RequestContext(request))
    #return HttpResponse(template_name.render(c))
"""

def ask(request):
    pass

def search(request):
    pass

def media(request, path):
    """
    response = serve(request, "%s/media/%s" % (skin, path),
                 document_root=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'skins').replace('\\', '/'))
    """
    response = serve(request, "/media/%s" % (path),
                 document_root=os.path.dirname(os.path.dirname(__file__)).replace('\\', '/'))
    content_type = response.get('Content-Type', '')
    if ('charset=' not in content_type):
        if (content_type.startswith('text') or content_type=='application/x-javascript'):
            content_type += '; charset=utf-8'
            response['Content-Type'] = content_type
    return response

"""
This function is to construct the input question list (i.e. initial) with pagination context and extra context,
so that the question list can be used (as dynamic data) to render the template.
"""
def question_list(request, initial,
                  list_description=_('questions'),
                  base_path=None,
                  page_title=_("All Questions"),
                  allowIgnoreTags=True,
                  feed_url=None,
                  paginator_context=None,
                  show_summary=None,
                  feed_sort=('-added_at',),
                  feed_req_params_exclude=(_('page'), _('pagesize'), _('sort')),
                  extra_context={}):

    if show_summary is None:
        show_summary = bool(settings.SHOW_SUMMARY_ON_QUESTIONS_LIST)

    #questions = initial.filter_state(deleted=False)
    questions = initial

    if request.user.is_authenticated() and allowIgnoreTags:
        pass
        """
        questions = questions.filter(~Q(tags__id__in = request.user.marked_tags.filter(user_selections__reason = 'bad')))
        """

    if page_title is None:
        page_title = _("Questions")

    """
    if request.GET.get('type', None) == 'rss':
        if feed_sort:
            questions = questions.order_by(*feed_sort)
        return RssQuestionFeed(request, questions, page_title, list_description)(request)
    """

    keywords =  ""
    if request.GET.get("q"):
        keywords = request.GET.get("q").strip()

    #answer_count = Answer.objects.filter_state(deleted=False).filter(parent__in=questions).count()
    #answer_description = _("answers")

    if not feed_url:
        req_params = generate_uri(request.GET, feed_req_params_exclude)

        if req_params:
            req_params = '&' + req_params

        feed_url = request.path + "?type=rss" + req_params

    context = {
        'questions' : questions.distinct(),
        'questions_count' : questions.count(),
        'keywords' : keywords,
        'list_description': list_description,
        'base_path' : base_path,
        'page_title' : page_title,
        'tab' : 'questions',
        'feed_url': feed_url,
        'show_summary' : show_summary,
    }
    context.update(extra_context)

    return pagination.paginated(request,
                               ('questions', paginator_context or QuestionListPaginatorContext()), context)
