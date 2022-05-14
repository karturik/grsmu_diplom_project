from django.shortcuts import render, redirect
from .models import Teacher, Department, Comment, Vote, CommentAnswer
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy, reverse
from .forms import CommentForm, VoteForm, CommentAnswerForm
from django.contrib import messages

# SEARCHING
from django.db.models import Q




# Create your views here.
# def main_page(request):
#     return render(request, 'demo_site/main_page.html')

def demo_site_index(request):
    department = Department.objects.order_by('title')
    context = {
        "departments": department,
    }
    return render(request, "demo_site/demo_site_index.html", context)

def demo_site_department(request, department):
    teachers = Teacher.objects.filter(department__title__contains=department)
    context = {
        "department": department,
        "teachers": teachers
    }
    return render(request, "demo_site/demo_site_department.html", context)

def demo_site_detail(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    comment_form = CommentForm()
    answer_form = CommentAnswerForm()
    vote_count = Vote.objects.filter(teacher=teacher).count()
    vote_form = VoteForm()
    vote_form.calculate_averages(teacher)
    comments = Comment.objects.filter(teacher=teacher).order_by('-created_on')
    votes = Vote.objects.filter(teacher=teacher, user=request.user)
    comment_answers = CommentAnswer.objects.filter(teacher=teacher)
    if not request.user.is_authenticated:
        group = 0
    else:
        group = str(request.user.groups.get())
    if request.method == "POST":
        if "comment_left" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = Comment(
                    author = request.user,
                    body = comment_form.cleaned_data['body'],
                    teacher = teacher
                )
                comment.save()
        elif "score_submit" in request.POST:
            vote_form = VoteForm(request.POST)
            if vote_form.is_valid():
                if votes:
                    for vote in votes:
                        vote_form = VoteForm(request.POST, instance=vote)
                else:
                    pass
                form = vote_form.save(commit=False)
                form.user = request.user
                form.teacher = teacher
                form.save()
                messages.success(request, (f'{form.teacher.name}, оценка сохранена'))
            else:
                messages.error(request,('Ошибка при сохранении оценки'))
        elif "comment_answer" in request.POST:
            answer_form = CommentAnswerForm(request.POST)
            if answer_form.is_valid():
                comment_pk = int(request.POST.get('comment_pk'))
                answer = CommentAnswer(author = request.user,
                    body = answer_form.cleaned_data['body'],
                    comment = Comment.objects.get(pk=comment_pk),
                    teacher=teacher)
                answer.save()
                # form = answer_form.save(commit=False)
                # form.author = request.user
                # pk = request.POST.get['comment.pk']
                # form.comment = Comment.objects.filter(pk=pk)
                # form.save()
        return redirect ('demo_site_detail', pk)
    context = {
        "teacher": teacher,
        "comments": comments,
        "comment_form": comment_form,
        "answer_form": answer_form,
        "vote_form": vote_form,
        "group": group,
        "vote_count": vote_count,
        "comment_answers": comment_answers,
        "votes": votes,
    }
    return render(request, "demo_site/demo_site_detail.html", context)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = 'demo_site/comment_deletion.html'
    def get_success_url(self):
        return reverse_lazy('demo_site_index')

    def test_func(self):
        comment = self.get_object()
        return str(self.request.user) == str(comment.author) or self.request.user.is_superuser

class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    fields = ['body']
    template_name = 'demo_site/comment_edit.html'
    def get_success_url(self):
        return reverse_lazy("demo_site_index")

    def test_func(self):
        comment = self.get_object()
        return str(self.request.user) == str(comment.author)

def searching(request):
    if request.method == "POST":
        searched = request.POST.get('searched').title()
        results = Teacher.objects.filter(name__icontains=searched)
        return render(request, "demo_site/search_page.html", {'searched':searched, "results":results})
    else:
        return render(request, "demo_site/search_page.html")


