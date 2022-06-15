from django.shortcuts import render, redirect

#notifications
from django.http import HttpResponse
from django.contrib.auth.models import User
from notifications.signals import notify
from django.contrib.admin.views.decorators import staff_member_required

def main_page(request):
    if request.method == "POST":
        user=request.user
        notification = user.notifications.unread()
        notification.delete()
    return render(request, 'grsmu_diplom/main_page.html')

@staff_member_required
def staff(request):
    users = User.objects.all()
    user = User.objects.get(id=request.user.id)
    return render(request, 'grsmu_diplom/messages.html', {'users': users, 'user': user})

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