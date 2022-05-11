from django.shortcuts import render, redirect
from .models import Teacher, Department, Comment, Vote
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy, reverse
from .forms import CommentForm, VoteForm
from django.contrib import messages




# Create your views here.
def demo_site_index(request):
    department = Department.objects.all()
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
    form = CommentForm()
    vote_count = Vote.objects.filter(teacher=teacher).count()
    vote_form = VoteForm()
    vote_form.calculate_averages(teacher)
    if not request.user.is_authenticated:
        group = 0
    else:
        group = str(request.user.groups.get())
    if request.method == "POST":
        if "comment_left" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment(
                    author = request.user,
                    body = form.cleaned_data['body'],
                    teacher = teacher
                )
                comment.save()
        elif "score_submit" in request.POST:
            vote_form = VoteForm(request.POST)
            if vote_form.is_valid():
                form = vote_form.save(commit=False)
                form.profile = request.user.profile
                form.teacher = teacher
                form.save()
                messages.success(request, (f'{form.teacher.name}, оценка сохранена'))
            else:
                messages.error(request,('Ошибка при сохранении оценки'))
        return redirect ('demo_site_detail', pk)
    comments = Comment.objects.filter(teacher=teacher).order_by('-created_on')
    context = {
        "teacher": teacher,
        "comments": comments,
        "form": form,
        "vote_form": vote_form,
        "group": group,
        "vote_count": vote_count
    }
    return render(request, "demo_site/demo_site_detail.html", context)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = 'demo_site/comment_deletion.html'
    def get_success_url(self):
        return reverse_lazy('demo_site_index')

    def test_func(self):
        comment = self.get_object()
        return str(self.request.user) == str(comment.author)

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
        searched = request.POST.get('searched')
        results = Teacher.objects.filter(name=searched)
        return render(request, "demo_site/search_page.html", {'searched':searched, "results":results})
    else:
        return render(request, "demo_site/search_page.html")


