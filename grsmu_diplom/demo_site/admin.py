from django.contrib import admin
from demo_site.models import Department, Teacher, Comment

# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    pass

class DepartmentAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Comment, CommentAdmin)