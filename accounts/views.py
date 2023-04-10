from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,render
from django.views import View
from record_officers.models import RecordOfficer
from student_affair_officers.models import StudentAffairOfficer
from students.models import Student, Department

from . forms import (StudentProfileFormView, UserFormView,
                     RecordOfficerProfileFormView, StudentAffairProfileFormView)
from . models import CustomUser
from .forms import LoginForm

# Create your views here.
def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin:index')
                elif user.user_type == "student":
                    return redirect('screening:index')
                elif user.user_type == "record_officer":
                    return redirect('record_officer:home')
                elif user.user_type == "student_affair":
                    return redirect('student_affair:home')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()

    template_name = 'screening/login.html'
    return render(request, template_name, context={'form':form})

def logout_request(request):
    logout(request)
    return redirect('accounts:login')

class ProfileView(LoginRequiredMixin, View):
    login_url = 'accounts:login'
    user_form = UserFormView
    template_name = 'screening/profile.html'

    def get(self, request):
        user = CustomUser.objects.get(email = request.user)
        user_form = self.user_form(instance=user)
        context = {'user_form':user_form}
        # form = self.form_class
        if user.user_type == 'student':
            user_details = Student.objects.get(user_id = request.user)
            student_form = StudentProfileFormView(request, instance=user_details)
            # student_form.fields['department_id'].queryset = Department.objects.filter(deptName = request.user.student.department_id)
            context['user_details'] = user_details
            context['student_form'] = student_form
        elif user.user_type == 'record_officer':
            user_details = RecordOfficer.objects.get(user_id = request.user)
            context['record_officer_form'] = RecordOfficerProfileFormView(request, instance=user_details)
        elif user.user_type == 'student_affair':
            user_details = StudentAffairOfficer.objects.get(user_id = request.user)
            context['student_affair_form'] = StudentAffairProfileFormView(request, instance=user_details)

        return render(request, self.template_name, context=context)
    
    def post(self, request):
        user = get_user_model().objects.get(email = request.user)
        user_form = self.user_form(instance=user)
        context = {'user_form':user_form}
        print(f"request: {request.POST}")
        try:
            user = get_user_model().objects.get(email = request.user)
            if user.user_type == 'student':
                user_details = Student.objects.get(user_id = request.user)
                context['student_form'] = StudentProfileFormView(request, request.POST, instance=user_details)
                if 'update_profile' in request.POST:
                    if context['student_form'].is_valid():
                        user = context['student_form'].save(commit=False)
                        user.save()
                        messages.success(request, 'Profile Updated')
                        return redirect('accounts:profile')
                    else:
                        print(f"Form error: {context['student_form'].errors}")
                        messages.error(request, f"An error occurred: {context['student_form'].errors}")
            elif user.user_type == 'record_officer':
                user_details = RecordOfficer.objects.get(user_id = request.user)
                context['record_officer_form'] = RecordOfficerProfileFormView(request, request.POST, instance=user_details)
                if 'update_profile' in request.POST:
                    if context['record_officer_form'].is_valid():
                        user = context['record_officer_form'].save(commit=False)
                        user.save()
                        messages.success(request, 'Profile Updated')
                        return redirect('accounts:profile')
                    else:
                        messages.error(request, "An error occurred")
            elif user.user_type == 'student_affair':
                user_details = StudentAffairOfficer.objects.get(user_id = request.user)
                context['student_affair_form'] = StudentAffairProfileFormView(request, request.POST, instance=user_details)
                if 'update_profile' in request.POST:
                    if context['student_affair_form'].is_valid():
                        user = context['student_affair_form'].save(commit=False)
                        user.save()
                        messages.success(request, 'Profile Updated')
                        return redirect('accounts:profile')
                    else:
                        
                        messages.error(request, "An error occurred")
            
            
            return render(request, self.template_name, context=context)
        except ObjectDoesNotExist:
            messages.error(request, "Account not found")
            return redirect('accounts:profile')

def UpdateProfile(request, id):
    try:
        user = get_user_model().objects.get(pk=id)
        if user.user_type == 'student':
            user_details = Student.objects.get(user_id = request.user)
            form = StudentProfileFormView(request, instance=user_details) 
        elif user.user_type == 'record_officer':
            user_details = RecordOfficer.objects.get(user_id = request.user)
            form = RecordOfficerProfileFormView(instance=user_details)
        elif user.user_type == 'student_affair':
            user_details = StudentAffairOfficer.objects.get(user_id = request.user)
            form = StudentAffairProfileFormView(instance=user_details)
        
        if 'update_profile' in request.POST:
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                messages.success(request, 'Profile Updated')
                return redirect('accounts:profile')
            messages.warning(request, "An error occurred")
    except ObjectDoesNotExist:
        messages.error(request, "Account not found")

class UpdateProfileView(LoginRequiredMixin, View):
    login_url = 'accounts:login'
    template_name = 'screening/profile.html'

    def get(self, request, id):
        context = {}
        try:
            user = get_user_model().objects.get(id=id)
            if user.user_type == 'student':
                user_details = Student.objects.get(user_id = request.user)
                student_form = StudentProfileFormView(request, instance=user_details)
                context['user_details'] = user_details
                context['student_form'] = student_form
            elif user.user_type == 'record_officer':
                user_details = RecordOfficer.objects.get(user_id = request.user)
                context['record_officer_form'] = RecordOfficerProfileFormView(instance=user_details)
            elif user.user_type == 'student_affair':
                user_details = StudentAffairOfficer.objects.get(user_id = request.user)
                context['student_affair_form'] = StudentAffairProfileFormView(instance=user_details)
            return render(request, self.template_name, context=context)
        except ObjectDoesNotExist:
            pass


