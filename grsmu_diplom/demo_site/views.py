from django.shortcuts import render, redirect
from .models import Teacher, Department, Comment, Vote, CommentAnswer
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy, reverse
from .forms import CommentForm, VoteForm, CommentAnswerForm
from django.contrib import messages

#PAGINATION
from django.core.paginator import Paginator

#Liks
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.http import JsonResponse

#SORTING
from django.db.models import Count


# Create your views here.
def demo_site_index(request):
    department = Department.objects.order_by('title')
    context = {
        "departments": department,
    }
    return render(request, "demo_site/demo_site_index.html", context)

def demo_site_department(request, pk):
    teachers = Teacher.objects.filter(department__pk=pk)
    department = Department.objects.get(pk=pk)
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
    #если юзер авторизован - получаем инфу о его оценке, если нет - оценки всех остальных
    if request.user.is_authenticated:
        votes = Vote.objects.filter(teacher=teacher, user=request.user)
    else:
        votes = Vote.objects.filter(teacher=teacher)
    #если юзер не авторизован, то его группы нет
    if not request.user.is_authenticated:
        group = 0
    else:
        group = str(request.user.groups.get())
    #после нажатия на кнопку
    if request.method == "POST":
        #кнопка "оставить комментарий"
        if "comment_left" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = Comment(
                    author = request.user,
                    body = comment_form.cleaned_data['body'],
                    teacher = teacher,
                    category = comment_form.cleaned_data['category'],
                )
                comment.save()
        #кнопка "оценить"
        elif "score_submit" in request.POST:
            vote_form = VoteForm(request.POST)
            #если юзер уже оценивал - меняем его имеющуюся оценку
            if vote_form.is_valid():
                if votes:
                    for vote in votes:
                        vote_form = VoteForm(request.POST, instance=vote)
                else:
                    vote_form = VoteForm(request.POST)
                form = vote_form.save(commit=False)
                form.user = request.user
                form.teacher = teacher
                form.save()
                messages.success(request, (f'{form.teacher.name}, оценка сохранена'))
            else:
                messages.error(request,('Ошибка при сохранении оценки'))
        #кнопка "ответить на комментарий"
        elif "comment_answer" in request.POST:
            answer_form = CommentAnswerForm(request.POST)
            if answer_form.is_valid():
                comment_pk = int(request.POST.get('comment_pk'))
                answer = CommentAnswer(author = request.user,
                    body = answer_form.cleaned_data['body'],
                    comment = Comment.objects.get(pk=comment_pk),
                    teacher=teacher)
                answer.save()
        #кнопка "удалить ответ"
        elif "answer_delete" in request.POST:
            answer_pk = request.POST.get('answer_pk')
            answer = CommentAnswer.objects.filter(pk=answer_pk)
            answer.delete()
        #кнопка "удалить комментарий"
        elif "comment_delete" in request.POST:
            comment_pk = request.POST.get('comment_pk')
            comment = Comment.objects.filter(pk=comment_pk)
            comment.delete()

        return redirect ('demo_site_detail', pk)

    # ФИЛЬТРЫ
    filter = request.GET.get("filter")
    if filter:
        if filter == "all":
            comments = Comment.objects.filter(teacher=teacher)
        else:
            comments = Comment.objects.filter(category=filter)

    # СОРТИРОВКА
    sort_by = request.GET.get("sort")
    if sort_by == "likes":
        comments = comments.annotate(cnt=Count('likes')).order_by('-cnt')

    elif sort_by == "date":
        comments = comments.order_by('created_on')

    elif sort_by == "-likes":
        comments = comments.annotate(cnt=Count('likes')).order_by('cnt')

    elif sort_by == "-date":
        comments = comments.order_by('-created_on')


    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    comment_answers = CommentAnswer.objects.filter(teacher=teacher)
    test = []
    for comment in comments:
        a = comment.AnswerFor.all()
        test.append(a)
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
        "page_obj": page_obj,
        "page_number": page_number,
        "sort_by": sort_by,
        "filter": filter,
        "test": test,
    }
    return render(request, "demo_site/demo_site_detail.html", context)


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

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def likes(request):
    user = request.user
    pk = request.POST.get('pk')
    comment = Comment.objects.get(pk=pk)
    if request.method == "POST":
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            is_liked = False
        else:
            comment.likes.add(request.user)
            comment.dislikes.remove(request.user)
            is_liked = True

    context = {
    "comment": comment,
    'is_liked': is_liked,
    'total_likes': comment.likes.count(),
    }
    if is_ajax(request=request):
        html = render_to_string('demo_site/like_section.html', context, request=request)
        return JsonResponse({'form': html})

def dislikes(request):
    user = request.user
    pk = request.POST.get('pk')
    comment = Comment.objects.get(pk=pk)
    if request.method == "POST":
        if comment.dislikes.filter(id=request.user.id).exists():
            comment.dislikes.remove(request.user)
            is_disliked = False
        else:
            comment.dislikes.add(request.user)
            comment.likes.remove(request.user)
            is_disliked = True

    context = {
    "comment": comment,
    'is_disliked': is_disliked,
    'total_likes': comment.dislikes.count(),
    }
    if is_ajax(request=request):
        html = render_to_string('demo_site/like_section.html', context, request=request)
        return JsonResponse({'form': html})

def comments(request):
    pk = request.POST.get('teacher_pk')
    teacher = Teacher.objects.get(pk=pk)
    answer_form = CommentAnswerForm()
    comments = Comment.objects.filter(teacher=teacher).annotate(cnt=Count('likes')).order_by('-cnt')
    paginator = Paginator(comments, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    comment_answers = CommentAnswer.objects.filter(teacher=teacher)
    #если юзер не авторизован, то его группы нет
    if not request.user.is_authenticated:
        group = 0
    else:
        group = str(request.user.groups.get())
    context = {
        "teacher": teacher,
        "comments": comments,
        "answer_form": answer_form,
        "group": group,
        "comment_answers": comment_answers,
        "page_obj": page_obj,
    }
    if request.method == "POST":
        if is_ajax(request=request):
            html = render_to_string('demo_site/comment_section.html', context, request=request)
            return JsonResponse({'form': html})
    return redirect('demo_site_detail', pk=1)

