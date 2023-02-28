from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse

from screening.models import FirstScreening


# Create your views here.
def homepage(request):
    return render(request, 'student_affair_officers/homepage.html', context={})

class FirstScreeningList(ListView):
    model = FirstScreening
    template_name = 'student_affair_officers/first_screening.html'
    context_object_name = "fscreening"

    #override get queryset method
    def get_queryset(self):
        return FirstScreening.objects.filter(status = 'pending for student affair')

class FirstScreeningDetail(DetailView):
    model = FirstScreening
    template_name = 'student_affair_officers/first_screening_detail.html'

def fscreening_modify(request, id):
    if request.method == 'POST':
        if request.POST.get('approve'):
            fscreening = FirstScreening.objects.get(id=id)
            fscreening.status = 'approved'
            fscreening.save()
            messages.success(request, 'Screening successfully approved')
        elif request.POST.get('reject'):
            if request.POST.get('comment') == '':
                messages.warning(request, 'Kindly comment reasons why you reject this screening')
                print('Kindly comment reasons why you reject this screening')
                #i'd like to return to the same page
                return redirect(request.path_info) #it's not working
            else:
                fscreening = FirstScreening.objects.get(id=id)
                fscreening.status = 'rejected'
                fscreening.comment = request.POST.get('comment')
                fscreening.save()
                messages.success(request, 'Screening successfully rejected')
    return redirect(reverse('student_affair:first_screening'))
    