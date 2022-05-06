from django import forms

# voting
from .models import Vote
from django.forms.widgets import NumberInput

class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(
        attrs = {
            "class": "form-control",
            "placeholder": "Оставьте комментарий!"
        })
    )

class VoteForm(forms.ModelForm):
    communication = forms.IntegerField(label='Коммуникация', widget=NumberInput(attrs={'placeholder': ('5'), 'type':'range', 'min':'1', 'max':'10', 'class':'communication'}))
    teaching = forms.IntegerField(label='Обучение', widget=NumberInput(attrs={'placeholder': ('5'), 'type':'range', 'min':'1', 'max':'10', 'class':'teaching'}))
    demanding = forms.IntegerField(label='Требовательность', widget=NumberInput(attrs={'placeholder': ('5'), 'type':'range', 'min':'1', 'max':'10', 'class':'demanding'}))

    class Meta:
        model = Vote
        fields = ('communication', 'teaching', 'demanding')