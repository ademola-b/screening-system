from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse

from screening.models import FirstScreening, SecondScreening
from students.models import Department

# Create your views here.
def homepage(request):
    return render(request, 'student_affair_officers/homepage.html', context={})

class FirstScreeningList(LoginRequiredMixin, ListView):
    model = FirstScreening
    template_name = 'student_affair_officers/first_screening.html'
    context_object_name = "fscreening"

    #override get queryset method
    def get_queryset(self):
        return FirstScreening.objects.filter(status__in = ['pending for student affair', 'approved'])

class FirstScreeningDetail(DetailView):
    model = FirstScreening
    template_name = 'student_affair_officers/first_screening_detail.html'

@login_required
def fscreening_modify(request, id):
    if request.method == 'POST':
        if request.POST.get('approve'):
            fscreening = FirstScreening.objects.get(id=id)
            fscreening.status = 'approved'
            fscreening.comment = 'Approved'
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
    
class SecondScreeningList(LoginRequiredMixin, ListView):
    model = SecondScreening
    template_name = 'student_affair_officers/second_screening.html'
    context_object_name = 'sscreening'

    def get_queryset(self):
        return SecondScreening.objects.filter(status__in = ['pending for student affair', 'approved'])

class SecondScreeningDetail(LoginRequiredMixin, DetailView):
    model = SecondScreening
    template_name = 'student_affair_officers/second_screening_detail.html'

@login_required
def sscreening_modify(request, id):
    if request.method == 'POST':
        #print(request.POST)
        if request.POST.get('approve'):
            screening = SecondScreening.objects.get(id=id)
            screening.status = 'approved'
            screening.comment = 'Approved'
            screening.save()
            messages.success(request, 'Second Screening has been approved')
        elif request.POST.get('reject'):
            screening = SecondScreening.objects.get(id=id)
            if request.POST.get('comment') == '':
                messages.warning(request, "Kindly state reasons why you are rejecting this request")
                print('Kindly state reasons why you are rejecting this request')
                return redirect('student_affair:second_screening_detail', screening.id)
            screening = SecondScreening.objects.get(id=id)
            screening.status = 'rejected'
            screening.comment = request.POST.get('comment')
            screening.save()
            messages.success(request, 'Screening rejected')

    return redirect(reverse('student_affair:second_screening'))

class DepartmentsView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'student_affair_officers/departments.html'
    context_object_name = 'departments'
    