from django import forms

# voting
from .models import Vote, Comment
from django.forms.widgets import NumberInput
from django.db.models import Sum


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(
        attrs = {
            "class": "form-control",
            "placeholder": "Оставьте комментарий!"
        })
    )
    class Meta:
        model = Comment
        fields = ('body', 'category',)

class CommentAnswerForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Ответить на комментарий"
            })
    )

class VoteForm(forms.ModelForm):
    communication = forms.IntegerField(label='Коммуникация (1-плохая, 10-отличная)', widget=NumberInput(attrs={'placeholder': ('5'), 'type':'range', 'min':'1', 'max':'10', 'class':'communication'}))
    teaching = forms.IntegerField(label='Обучение (1-плохое, 10-отличное)', widget=NumberInput(attrs={'placeholder': ('5'), 'type':'range', 'min':'1', 'max':'10', 'class':'teaching'}))
    demanding = forms.IntegerField(label='Требовательность (1-высокая, 10-низкая)', widget=NumberInput(attrs={'placeholder': ('5'), 'type':'range', 'min':'1', 'max':'10', 'class':'demanding'}))

    class Meta:
        model = Vote
        fields = ('communication', 'teaching', 'demanding')

    def calculate_averages(self, teacher):
        vote_qs = Vote.objects.filter(teacher=teacher)
        vote_count = vote_qs.count()
        if vote_count != 0:
            communication_total = vote_qs.aggregate(Sum('communication'))
            teaching_total = vote_qs.aggregate(Sum('teaching'))
            demanding_total = vote_qs.aggregate(Sum('demanding'))
            teacher.communication_average = round(communication_total['communication__sum']/vote_count, 1)
            teacher.teaching_average = round(teaching_total['teaching__sum']/vote_count, 1)
            teacher.demanding_average = round(demanding_total['demanding__sum']/vote_count, 1)
            teacher.save()
        else:
            teacher.communication_average = 0.0
            teacher.teaching_average = 0.0
            teacher.demanding_average = 0.0
            teacher.save()