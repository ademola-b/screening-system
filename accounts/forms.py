from django import forms
from record_officers.models import RecordOfficer
from student_affair_officers.models import StudentAffairOfficer
from students.models import Student, Department, Level

from . models import CustomUser

class LoginForm(forms.Form):
    email = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'id': 'email','class':'form-control', 'placeholder':'Enter your email address', 'autofocus': 'true'}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'id':'password','class':'form-control', 'placeholder':'***********'}))

class UserFormView(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']

        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control', 'id':'basic-default-name', 'readonly':'readonly'}),
            'last_name':forms.TextInput(attrs={'class':'form-control', 'id':'basic-default-name', 'readonly':'readonly'}),
        
        }

class StudentProfileFormView(forms.ModelForm):
    department_id = forms.ModelChoiceField(queryset=Department.objects.none(), 
                                           empty_label=None, 
                                           widget = forms.Select(
                                            attrs={'class':'form-select','id':'exampleFormControlSelect1'}))
    
    level_id = forms.ModelChoiceField(queryset=Level.objects.none(), 
                                           empty_label=None, 
                                           widget = forms.Select(
                                            attrs={'class':'form-select','id':'exampleFormControlSelect1'}))
    class Meta:
        model = Student
        fields = ['application_no', 'level_id','department_id',
                  'phone_no', 'address', 'gender', 'dob']
        
        widgets = {
            'application_no':forms.TextInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
            'level_id':forms.TextInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
            'phone_no':forms.TextInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
            'address':forms.TextInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
            'gender':forms.TextInput(attrs={'class':'form-control', 'id':'basic-default-name', 'readonly':'readonly'}),
            'dob':forms.TextInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
        }

    def __init__(self, request, *args, **kwargs):
        super(StudentProfileFormView, self).__init__(*args, **kwargs)

        print(request.user.student.department_id)
        self.fields['level_id'].queryset = Level.objects.filter(levelInit = request.user.student.level_id)
        self.fields['department_id'].queryset = Department.objects.filter(deptName = request.user.student.department_id)

class RecordOfficerProfileFormView(forms.ModelForm):
    class Meta:
        model = RecordOfficer

        fields = ['department_id', 'phone_no', 'profile_pic']

        widgets = {
            'department_id':forms.TextInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
            'phone_no':forms.TextInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
        }

class StudentAffairProfileFormView(forms.ModelForm):
    class Meta:
        model = StudentAffairOfficer

        fields = ['phone_no', 'profile_pic']

        widgets = {
            # 'department_id':forms.TextInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
            'phone_no':forms.TextInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
        }


