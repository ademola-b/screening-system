from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect,render
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