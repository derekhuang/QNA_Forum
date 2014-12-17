import re
from django.db import models
from django.utils.html import strip_tags
from django.contrib.auth.models import User as DjangoUser, AnonymousUser as DjangoAnonymousUser
from django.utils.http import urlquote  as django_urlquote
from django.template.defaultfilters import slugify
from questions.settings.view import *

# Create your models here.
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'questions'
    
    def __str__(self):
        return self.description
    
    """
    Without this method, the Chinese characters can't be displayed correctly
    """
    def __unicode__(self):
        return self.description
    
class Node(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=50)
    body = models.TextField()
    published_time = models.DateTimeField()
    view_amount = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return self.body
    
    def __unicode(self):
        return self.body
    
    @property
    def user(self):
        return self.author

    @property
    def html(self):
        return self.body
    
    class Meta:
        abstract = True

class Question(Node):
    """ The associated stock """
    stock_id = models.CharField(max_length=10)
    
    title = models.CharField(max_length=100) 
    
    """ 3-levels classes for each question """
    catetory = models.IntegerField()
    tag = models.ForeignKey(Tag) 
    sub_tag = models.IntegerField(blank=True)

    like = models.IntegerField(default=0)
    
    @property
    def summary(self):
        content = strip_tags(self.html)

        # Remove multiple spaces.
        content = re.sub(' +',' ', content)

        # Replace line breaks with a space, we don't need them at all.
        content = content.replace("\n", ' ')

        # Truncate and all an ellipsis if length greater than summary length.
        content = (content[:SUMMARY_LENGTH] + '...') if len(content) > SUMMARY_LENGTH else content

        return content
    
    @property
    def headline(self):
        title = self.title

        # Replaces multiple spaces with single ones.
        title = re.sub(' +',' ', title)

        return title
    
    """
    TBD: To be updated to calculate the correct count of associated answers.
    """
    @property
    def answer_count(self):
        return 0
    
    @models.permalink    
    def get_absolute_url(self):
        return ('question', (), {'id': self.id, 'slug': django_urlquote(slugify(self.title))})
    
    class Meta:
        app_label = 'questions'
    
class Answer(Node):
    question = models.ForeignKey(Question)

    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'questions'
    
class Comment(Node):
    answer = models.ForeignKey(Answer)
    
    class Meta:
        app_label = 'questions'

    
class AnonymousUser(DjangoAnonymousUser):
    reputation = 0
    
    def get_visible_answers(self, question):
        return question.answers.filter_state(deleted=False)

    def can_view_deleted_post(self, post):
        return False

    def can_vote_up(self):
        return False

    def can_vote_down(self):
        return False
    
    def can_vote_count_today(self):
        return 0

    def can_flag_offensive(self, post=None):
        return False

    def can_view_offensive_flags(self, post=None):
        return False

    def can_comment(self, post):
        return False

    def can_like_comment(self, comment):
        return False

    def can_edit_comment(self, comment):
        return False

    def can_delete_comment(self, comment):
        return False

    def can_convert_to_comment(self, answer):
        return False
    
    def can_convert_to_question(self, answer):
        return False
    
    def can_convert_comment_to_answer(self, comment):
        return False

    def can_accept_answer(self, answer):
        return False

    def can_create_tags(self):
        return False

    def can_edit_post(self, post):
        return False

    def can_wikify(self, post):
        return False

    def can_cancel_wiki(self, post):
        return False

    def can_retag_questions(self):
        return False

    def can_close_question(self, question):
        return False

    def can_reopen_question(self, question):
        return False

    def can_delete_post(self, post):
        return False

    def can_upload_files(self):
        return False

    def is_a_super_user_or_staff(self):
        return False

    
    
    