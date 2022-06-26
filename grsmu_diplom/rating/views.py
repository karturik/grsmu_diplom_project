from django.shortcuts import render
import requests
from demo_site.models import Department, Teacher, Comment
from django.contrib.auth.models import User
from django.db.models import Avg, Min, Max, Count, Q, Sum

# Create your views here.
def rating_main_page(request):
    #самый закомменченный и оцененный преподы
    most_comment_teachers = Teacher.objects.annotate(count=Count('CommentFor')).order_by('-count')[0:3]
    most_votes_teachers = Teacher.objects.annotate(count=Count('VoteFor')).order_by('-count')[0:3]
    #самая комментируемая кафедра
    comment_departments = Teacher.objects.values('department').annotate(count=Count('CommentFor')).order_by('-count')[0:3]
    most_comment_departments = {}
    for department in comment_departments:
        com_dep = Department.objects.get(id=department["department"])
        most_comment_departments[com_dep]=department["count"]
    #самая оцененная кафедра
    votes_departments = Teacher.objects.values('department').annotate(count=Count('VoteFor')).order_by('-count')[0:3]
    most_votes_departments = {}
    for department in votes_departments:
        votes_dep = Department.objects.get(id=department["department"])
        most_votes_departments[votes_dep]=department["count"]
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

    context ={
        "most_comment_teachers":most_comment_teachers,
        "most_votes_teachers":most_votes_teachers,
        "most_comment_user":most_comment_user,
        "most_votes_user":most_votes_user,
        "most_liked_comment":most_liked_comment,
        "most_comment_departments":most_comment_departments,
        "most_votes_departments":most_votes_departments,
        "most_liked_users":most_liked_users,
    }
    return render(request, 'rating/rating_main_page.html', context)

def rating_departments(request):
    average_department_vote = 0
    # по кафедрам
    departments = 0
    # по курсам
    pass