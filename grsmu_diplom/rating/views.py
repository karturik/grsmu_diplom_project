from django.shortcuts import render
import requests
from demo_site.models import Department, Teacher, Comment, Vote
from django.contrib.auth.models import User
from django.db.models import Avg, Min, Max, Count, Q, Sum

# Create your views here.
def rating_main_page(request):
    #самый закомменченный и оцененный преподы
    most_comment_teachers = Teacher.objects.annotate(count=Count('CommentFor')).order_by('-count')[0:3]
    most_votes_teachers = Teacher.objects.annotate(count=Count('VoteFor')).order_by('-count')[0:3]

    #больше всего комментов оставили
    most_comment_user = User.objects.annotate(count=Count('CommentFrom')).order_by('-count')[0:3]
    #больше всего оценок поставили
    most_votes_user = User.objects.annotate(count=Count('VoteFrom')).order_by('-count')[0:3]
    #самые залайканные комментарии
    most_liked_comment = Comment.objects.annotate(count=Count('likes')).order_by('-count')[0:3]
    #юзеры, больше всего лайков собрали
    liked_users = Comment.objects.values('author').annotate(count=Count('likes')).order_by('-count')[0:3]
    most_liked_users = {}
    for user in liked_users:
        liked_user = User.objects.get(id=user["author"])
        most_liked_users[liked_user] = user["count"]
    users_count = User.objects.all().count()
    comments_count = Comment.objects.all().count()
    votes_count = Vote.objects.all().count() * 3

    context ={
        "most_comment_teachers":most_comment_teachers,
        "most_votes_teachers":most_votes_teachers,
        "most_comment_user":most_comment_user,
        "most_votes_user":most_votes_user,
        "most_liked_comment":most_liked_comment,
        "most_liked_users":most_liked_users,
        "users_count":users_count,
        "comments_count":comments_count,
        "votes_count":votes_count,
    }
    return render(request, 'rating/rating_main_page.html', context)

def rating_departments_page(request):
    departments = Department.objects.all()

    # самая комментируемая кафедра
    comment_departments = Teacher.objects.values('department').annotate(comment_count=Count('CommentFor')).order_by('-comment_count')[0:3]
    most_comment_departments = {}
    for department in comment_departments:
        com_dep = Department.objects.get(id=department["department"])
        most_comment_departments[com_dep] = department["comment_count"]

    # самая оцененная кафедра
    votes_departments = Teacher.objects.values('department').annotate(votes_count=Count('VoteFor')).order_by('-votes_count')[0:3]
    most_votes_departments = {}
    for department in votes_departments:
        votes_dep = Department.objects.get(id=department["department"])
        most_votes_departments[votes_dep] = department["votes_count"]

    context = {
        "departments": departments,
        "most_comment_departments": most_comment_departments,
        "most_votes_departments": most_votes_departments,
    }
    return render(request, 'rating/rating_departments_page.html', context)

def rating_department_detail_page(request, pk):
    department = Department.objects.get(pk=pk)
    # average_vote of department
    all_comment_teachers = Teacher.objects.filter(department=department).annotate(count=Count('CommentFor')).exclude(count=0).order_by('-count')
    # all_comment_teachers = Teacher.objects.filter(department=department).annotate(count=Count('CommentFor')).order_by('-count')
    top_comment_teachers = all_comment_teachers[0:3]
    comment_teachers = all_comment_teachers[3:]
    all_votes_teachers = Teacher.objects.filter(department=department).annotate(count=Count('VoteFor')).exclude(count=0).order_by('-count')
    top_votes_teachers = all_votes_teachers[0:3]
    votes_teachers = all_votes_teachers[3:]

    context={
        "pk":pk,
        "department":department,
        "top_comment_teachers":top_comment_teachers,
        "comment_teachers":comment_teachers,
        "top_votes_teachers":top_votes_teachers,
        "votes_teachers":votes_teachers,

    }
    return render(request, 'rating/rating_department_detail_page.html', context)