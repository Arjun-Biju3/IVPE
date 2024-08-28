from django.shortcuts import render

def cwadminHome(request):
    return render(request,'index3.html')

def add_candidates(request):
    return render(request,'add_candidates.html')

def change_password(request):
    return render(request,'change_password.html')
    