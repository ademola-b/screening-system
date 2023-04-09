from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View, ListView

from . forms import (FirstScreeningUpload, SecondScreeningUpload, )
from . models import FirstScreening
from . models import SecondScreening
# Create your views here.

def homepage(request):
    return render(request, 'screening/homepage.html', context={})

@login_required
def index(request):
    try:
        fscreening = FirstScreening.objects.get(student_id=request.user.student.firstscreening.student_id)
    except:
        fscreening = None

    try:
        sscreening = SecondScreening.objects.get(student_id=request.user.student.secondscreening.student_id)
    except:
        sscreening = None

    return render(request, 'screening/index.html', context={'fscreening':fscreening, 'sscreening':sscreening})

class FirstScreeningForm(LoginRequiredMixin, View):
    form_class = FirstScreeningUpload
    template_name = 'screening/first-screening.html'

    #load an empty form when page first load
    def get(self, request): 
        form = self.form_class()            
        return render(request, self.template_name, context={'form':form})

    def post(self, request):
        # get the details filled in form
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            fsc = FirstScreening.objects.filter(student_id=request.user.student).exists() #check if record exists, update if yes
            if fsc:
                rec = FirstScreening.objects.get(student_id=request.user.student)
                rec.o_level = form.cleaned_data.get('o_level')
                rec.indigene_certificate = form.cleaned_data.get('indigene_certificate')
                rec.pry_certificate = form.cleaned_data.get('pry_certificate')
                rec.ND_result = form.cleaned_data.get('ND_result')
                rec.admission_letter = form.cleaned_data.get('admission_letter')
                rec.acceptance_fee_receipt = form.cleaned_data.get('acceptance_fee_receipt')
                rec.status = 'pending for record officer'
                rec.comment = 'pending for record officer'
                rec.save()
                messages.success(request, "Request sent, kindly wait for approval")
                return redirect('screening:index')
            else:
                form = form.save(commit=False)
                form.student_id = request.user.student
                form.status = 'pending for record officer'
                form.save()
                messages.success(request, "Request sent, kindly wait for approval")
                return redirect('screening:index')
        else:
            messages.warning(request, f"An error occurred: {form.errors.as_text}")

        return render(request, self.template_name, context={'form':form})

class FirstScreeningView(ListView):
    model = FirstScreening
    allow_empty = False
    context_object_name = 'firstScreening'
    template_name = 'screening/first-screening-status.html'

    def get_queryset(self, **kwargs): #not using this because this method doesn't return HTTPResponse
        try: #check if user has done first screening
            student = self.request.user.student.firstscreening.student_id
            qs = FirstScreening.objects.get(student_id=student)
            return qs
        except:
            return redirect('screening:first_screening')

@login_required
def firstScreeningView(request):
    try:
        fscreening = FirstScreening.objects.get(student_id=request.user.student.firstscreening.student_id)
    except:
        messages.error(request, "You haven't done the first screening")
        return redirect('screening:first_screening')

    return render(request, template_name='screening/first-screening-status.html', context={'fscreening':fscreening})

@login_required
def secondScreeningView(request):
    try:
        fscreening = FirstScreening.objects.get(student_id=request.user.student.firstscreening.student_id)
        sscreening = SecondScreening.objects.get(student_id=request.user.student.secondscreening.student_id)     
    except FirstScreening.DoesNotExist:
        messages.error(request, 'First screening does not exist!')
        return redirect('screening:first_screening')
    except SecondScreening.DoesNotExist:
        return redirect('screening:second_screening')

    return render(request, template_name='screening/second-screening-status.html', context={'fscreening':fscreening,'sscreening':sscreening})
        
class SecondScreeningForm(View):
    form_class = SecondScreeningUpload
    template_name = 'screening/second-screening.html'

    def get(self, request):
        #on first load of page
        form = self.form_class()
        
        try:
          
            fscreening = FirstScreening.objects.get(student_id = request.user.student.firstscreening.student_id)
            # if not fscreening:
            #     messages.warning(request, 'No record of first screening')
                # return redirect('screening:index')
            if  fscreening.status != 'approved':
                messages.warning(request, 'Your first screening has not been approved')
                return redirect('screening:index') 
        except:
            messages.error(request, "An error occurred, Kindly login")
            return redirect('accounts:login')
       
        return render(request, self.template_name, context={'form':form})

    def post(self, request):
        #get form details from request FirstScreening.student_id.id
        form = self.form_class(request.POST, request.FILES)
        
        try:
            fscreening = FirstScreening.objects.get(student_id = request.user.student.firstscreening.student_id)
            print(fscreening)
            if not fscreening:
                messages.warning(request, "You have not done your first screening, kindly do so now.")
                return redirect('screening:first_screening')
            else:  
                if fscreening.status != 'approved':
                    messages.warning(request, 'Your first screening has not been approved')
                    return redirect('screening:index')
        except:
            return redirect('accounts:login')

        if form.is_valid():
            ssc = SecondScreening.objects.filter(student_id=request.user.student).exists()
            print(f"form: {form}")
            if ssc:
                rec = SecondScreening.objects.get(student_id = request.user.student)
                rec.first_screening = fscreening
                rec.acceptance_form = form.cleaned_data['acceptance_form']
                rec.school_fee_receipt = form.cleaned_data['school_fee_receipt']
                rec.medical_receipt = form.cleaned_data['medical_receipt']
                rec.entrepreneur_receipt = form.cleaned_data['entrepreneur_receipt']
                rec.jamb_admission_letter = form.cleaned_data['jamb_admission_letter']
                rec.jamb_original_result = form.cleaned_data['jamb_original_result']
                rec.attestation_letter = form.cleaned_data['attestation_letter']
                rec.status = 'pending for record officer'
                rec.comment = 'pending for record officer'
                rec.save()
                messages.success(request, "Documents submitted, Kindly wait for approval")
                return redirect('screening:index')
            else:
                form_data = form.save(commit=False)
                form_data.student_id = request.user.student
                form_data.first_screening = fscreening
                form_data.status = 'pending for record officer'
                form_data.save()
                messages.success(request, 'Documents submitted, Kindly wait for approval')
                return redirect('screening:index')
        else:
            messages.danger(request, f"An error occurred: {form.errors.as_text}")
        
        return render(request, self.template_name, context={'form':form})





    
        
        
        
    

