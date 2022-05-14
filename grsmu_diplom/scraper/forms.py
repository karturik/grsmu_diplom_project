from django import forms
from demo_site.models import Department, Teacher

# IMAGE SCRAPING
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import os
from django.template.defaultfilters import slugify
from django.core.files import File



class DepartmentAddForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['title']
        title = forms.CheckboxInput()

class TeacherAddForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'position', 'department']

# class TeacherImageAddForm(forms.ModelForm):
#     class Meta:
#         model = Teacher
#         fields = ['teacher_img', 'image_src']

# class TeacherImageAddForm(forms.ModelForm):
#     image_url = forms.URLField(required=False)
#
#     def clean(self, *args, **kwargs):
#         all_data = self.cleaned_data
#         url = all_data['image_url']
#         image = all_data['teacher_img']
#
#         if not image and url:
#             img_temp = NamedTemporaryFile(delete=True)
#             img_temp.write(urlopen(url).read())
#             img_temp.flush()
#             all_data['teacher_img'] = File(img_temp)
#
#         return all_data
#
#     class Meta:
#         model = Teacher
#         fields = ('teacher_img', )