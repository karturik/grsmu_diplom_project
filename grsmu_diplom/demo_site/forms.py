from django import forms

# voting
from .models import Vote, Teacher
from django.forms.widgets import NumberInput
from django.db.models import Sum


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

    def calculate_averages(self, teacher):
        vote_qs = Vote.objects.filter(teacher=teacher)
        vote_count = vote_qs.count()
        if vote_count != 0:
            communication_total = vote_qs.aggregate(Sum('communication'))
            teaching_total = vote_qs.aggregate(Sum('teaching'))
            demanding_total = vote_qs.aggregate(Sum('demanding'))
            teacher.communication_average = communication_total['communication__sum']/vote_count
            teacher.teaching_average = teaching_total['teaching__sum']/vote_count
            teacher.demanding_average = demanding_total['demanding__sum']/vote_count
            teacher.save()
        else:
            teacher.communication_average = 0.0
            teacher.teaching_average = 0.0
            teacher.demanding_average = 0.0
            teacher.save()