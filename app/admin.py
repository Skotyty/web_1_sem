from django.contrib import admin
# Register your models here.

from .models import Profile, Tag, Like, Question, Answer

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'description')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'value')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date_of_creation')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'correct', 'date_of_creation')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
