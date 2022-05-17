from django.shortcuts import render, redirect

def main_page(request):
    return render(request, 'grsmu_diplom/main_page.html')