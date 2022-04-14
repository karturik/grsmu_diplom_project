from django.shortcuts import render
from demo_site.models import Teacher, Department, Comment
from .forms import CommentForm

# Create your views here.
def demo_site_index(request):
    teachers = Teacher.objects.all()
    context = {
        "teachers": teachers,
    }
    return render(request, "demo_site_index.html", context)

def demo_site_department(request, department):
    teachers = Teacher.objects.filter(
        departments__title__contains=department
    )
    context = {
        "department": department,
        "teachers": teachers
    }
    return render(request, "demo_site_department.html", context)

def demo_site_detail(request, pk):
    teacher = Teacher.objects.get(pk=pk)

    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author= form.cleaned_data['author'],
                body = form.cleaned_data['body'],
                teacher = teacher
            )
            comment.save()
    comments = Comment.objects.filter(teacher=teacher)
    context = {
        "teacher": teacher,
        "comments": comments,
        "form": form,
    }
    return render(request, "demo_site_detail.html", context)
