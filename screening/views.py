from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View, ListView

from accounts.models import CustomUser
from students.models import Student

from . forms import FirstScreeningUpload, SecondScreeningUpload
from . models import FirstScreening
from . models import SecondScreening
# Create your views here.

def onboard(request):
    return render(request, 'screening/onboard.html', context={})

@login_required()
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


class FirstScreeningForm(View):
    form_class = FirstScreeningUpload
    template_name = 'screening/first-screening.html'

    #load an empty form when page first load
    def get(self, request): 
        form = self.form_class()

        try:
            form.fields['student_id'].queryset = Student.objects.filter(application_no=request.user.student.application_no) #get the logged in user's email address
            if not form.fields['student_id']: #user not logged in, login now
                messages.error(request, 'User not logged in')
                return redirect('accounts:login')
        except CustomUser.DoesNotExist:
            messages.error(request, 'An error occured, login now')
            return redirect('accounts:login')
            
        return render(request, self.template_name, context={'form':form})

    def post(self, request):
        # get the details filled in form
        form = self.form_class(request.POST, request.FILES)
        form.fields['student_id'].queryset = Student.objects.filter(application_no=request.user.student.application_no)
        if form.fields['student_id'].queryset:
            if form.is_valid():
                FirstScreening.status = 'pending for record officer'
                form.save()
                messages.success(request, "Request sent, kindly wait for approval")
                return redirect('screening:index')
            else:
                messages.error(request, 'An error occured')
        else:
            messages.error(request, 'Student details not found, kndly login')
            return redirect('accounts:login')
        
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

def firstScreeningView(request):
    try:
        fscreening = FirstScreening.objects.get(student_id=request.user.student.firstscreening.student_id)
    except:
        messages.error(request, "You haven't done the first screening")
        return redirect('screening:first_screening')

    return render(request, template_name='screening/first-screening-status.html', context={'fscreening':fscreening})

def secondScreeningView(request):
    try:
        fscreening = FirstScreening.objects.get(student_id=request.user.student.firstscreening.student_id)
        sscreening = SecondScreening.objects.get(student_id=request.user.student.secondscreening.student_id)     
    except FirstScreening.DoesNotExist:
        messages.error(request, 'First screening hasa not been approved!')
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
        
        #get user details
    #    FirstScreening.objects.get(student_id=request.user.student.firstscreening.student_id)
    # request.user.student.id
        
        try:
            form.fields['student_id'].queryset = Student.objects.filter(application_no = request.user.student.application_no)
            form.fields['first_screening'].queryset = FirstScreening.objects.filter(student_id = request.user.student.firstscreening.student_id) #set the user first_screening details
            if not form.fields['first_screening']:
                messages.error(request, 'First Screening Record not found')
                return redirect('screening:first_screening')
            elif not form.fields['student_id']:
                messages.error(request, 'Account not found, Kindly login now')
                return redirect('account:login')
            
        except:
            messages.error(request, 'An error occurred, Kindly login')
            return redirect('accounts:login')
       
        return render(request, self.template_name, context={'form':form})

    def post(self, request):
        #get form details from request FirstScreening.student_id.id
        form = self.form_class(request.POST, request.FILES)
        
        try:
            form.fields['student_id'].queryset = Student.objects.filter(application_no = request.user.student.application_no)
            form.fields['first_screening'].queryset = FirstScreening.objects.filter(student_id = request.user.student.firstscreening.student_id) #set the user first_screening details 
        except:
            return redirect('accounts:login')

        if form.fields['student_id'].queryset:
            if form.is_valid():
                form_data = form.save(commit=False)
                form_data.status = 'pending for record officer'
                form_data.save()
                messages.success(request, 'Documents submitted, wait for approval')
                return redirect('screening:index')
        else:
            messages.error(request, 'User has not done first screening')
            return redirect('screening:first_screening')
        
        return render(request, self.template_name, context={'form':form})

        
        
        
    

