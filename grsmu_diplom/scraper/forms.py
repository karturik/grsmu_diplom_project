from django import forms
from demo_site.models import Department, Teacher

class DepartmentAddForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['title']
        title = forms.CheckboxInput()

class TeacherAddForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'position', 'department']