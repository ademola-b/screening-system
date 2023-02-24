from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView

from screening.models import FirstScreening

# Create your views here.
@login_required
def homepage(request):
    return render(request, 'record_officers/homepage.html', context={})


class FirstScreeningList(LoginRequiredMixin, ListView):
    model = FirstScreening
    template_name = 'record_officers/first_screening.html'
    context_object_name = 'fscreening'

    def get_queryset(self):

        return FirstScreening.objects.filter(student_id__department_id__deptName=self.request.user.recordofficer.department_id.deptName)
    


class FirstScreeningDetail(DetailView):
    model = FirstScreening
    template_name = 'record_officers/screening_detail.html'

def record_officer_modify(request, id):
    if request.method == 'POST':
        if request.POST.get('approve'):
            screening = FirstScreening.objects.get(id=id)
            screening.status = 'Approved'
            screening.save()
        elif request.POST.get('reject'):
            screening = FirstScreening.objects.get(id=id)
            screening.status = 'Rejected'
            screening.save()

    return redirect(reverse('record_officer: screening_detail'))
  

    


    
