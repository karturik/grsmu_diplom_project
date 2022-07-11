from django.contrib import admin
from demo_site.models import Department, Teacher, Comment, Vote, CommentAnswer
from users.models import Profile
from moodle_test.models import Question, Answer
from proxie.models import Proxie

# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    pass

class DepartmentAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

class VoteAdmin(admin.ModelAdmin):
    pass

class CommentAnswerAdmin(admin.ModelAdmin):
    pass

class ProfileAdmin(admin.ModelAdmin):
    pass

class QuestionAdmin(admin.ModelAdmin):
    pass

class AnswerAdmin(admin.ModelAdmin):
    pass

class ProxieAdmin(admin.ModelAdmin):
    pass


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(CommentAnswer, CommentAnswerAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Proxie, ProxieAdmin)
