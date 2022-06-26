from django.shortcuts import render, redirect


def main_page(request):
    if request.method == "POST":
        user=request.user
        notification = user.notifications.unread()
        notification.delete()
    return render(request, 'grsmu_diplom/main_page.html')
