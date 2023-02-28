from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.

def homepage(request):
    return render(request, 'student_affair_officers/homepage.html', context={})