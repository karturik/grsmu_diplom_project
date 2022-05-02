from django import forms
from .models import Department

class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(
        attrs = {
            "class": "form-control",
            "placeholder": "Оставьте комментарий!"
        })
    )

class DepartmentAddForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['title']