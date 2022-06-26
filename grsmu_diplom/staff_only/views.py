from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

#comments
from demo_site.models import Comment, CommentAnswer

#notifications
from notifications.signals import notify


@staff_member_required
def staff(request):
    comments_count = Comment.objects.filter(checked=False).count()
    # comments_answers_count = CommentAnswer.objects.filter(checked=False).count()
    return render(request, "staff_only/staff_only_main.html", {'comment_count':comments_count})

@staff_member_required
def notification(request):
    users = User.objects.all()
    user = User.objects.get(id=request.user.id)
    return render(request, "staff_only/messages.html", {'users': users, 'user': user})

@staff_member_required
def message(request):
    try:
        if request.method == 'POST':
            sender = User.objects.get(id=request.user.id)
            if request.POST.get('send_to_all'):
                receiver = User.objects.all()
            elif request.POST.get('send_to_user'):
                username = request.POST.get('send_to_user')
                print(username)
                receiver = User.objects.filter(username=username)
            verb = request.POST.get('verb')
            notify.send(sender, recipient=receiver, verb=verb, description=request.POST.get('message'))
            return HttpResponse("Отправлено!")
        else:
            return HttpResponse("Запрос не POST")
    except Exception as e:
        return HttpResponse("Какая-то ошибка:", e)

@staff_member_required
def comments_moderation(request):
    comments = Comment.objects.filter(checked=False).order_by('created_on')
    context = {
        'comments':comments
    }
    return render(request, "staff_only/comments_moderation.html", context)

@staff_member_required
def comment_delete(request):
    pk = request.POST.get("comment_pk")
    try:
        comment = Comment.objects.get(id=pk)
        user = comment.author
    except:
        return HttpResponse("Такого комментария нет, возможно он уже был удален.")
    action = request.POST.get('action')
    if action == "delete_only":
        comment.delete()

        notify.send(sender=User.objects.get(id=request.user.id), recipient=user,
                    verb='Предупреждение',
                    description=f'Комментарий "{comment.body}" удален администратором за неприемлемое содержание! Предупреждений:{user.profile.warnings}/3')
        return HttpResponse(f"Коммент удален.")
    elif action == "delete_and_warning":
        comment.delete()
        user.profile.warnings += 1
        user.save()
        user.profile.warnings_delete(user.profile)
        notify.send(sender=User.objects.get(id=request.user.id), recipient=user,
                    verb='Предупреждение',
                    description=f'Комментарий "{comment.body}" удален за нарушение правил, +1 предупреждение! Предупреждений:{user.profile.warnings}/3')
        return HttpResponse(f"Коммент удален, вынесено предупреждение.")
    elif action == "checked":
        comment.checked = True
        comment.save()
        return HttpResponse(f"Коммент проверен.")
    return HttpResponse(f"Хз, что")