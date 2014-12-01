from django.contrib import admin
from questions.models import Question, Answer, Comment, Tag, KeyValue

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_time')
    list_filter = ['published_time']
    search_fields = ['title'] 

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(KeyValue)