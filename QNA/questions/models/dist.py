from django.db import models
from django.contrib.auth.models import User as DjangoUser, AnonymousUser as DjangoAnonymousUser

# Create your models here.
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'questions'
    
    def __str__(self):
        return self.description
    
class Node(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=50)
    body = models.TextField()
    published_time = models.DateTimeField()
    view_amount = models.IntegerField(default=0)
    
    def __str__(self):
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

    
    
    