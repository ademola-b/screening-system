from django import forms
from accounts.models import CustomUser

from students.models import Student
from . models import FirstScreening
from . models import SecondScreening

class FirstScreeningUpload(forms.ModelForm):
    # student_id = forms.ModelChoiceField(queryset=Student.objects.none(), empty_label=None)
    
    class Meta:
        model = FirstScreening

        fields = ['o_level', 'indigene_certificate', 'pry_certificate', 
                    'ND_result', 'admission_letter', 'acceptance_fee_receipt']

        # widgets = {
        #     'student_id':forms.Select(attrs={'hidden':'hidden'})
        # }

class SecondScreeningUpload(forms.ModelForm):
    student_id = forms.ModelChoiceField(queryset=Student.objects.none(), empty_label=None)
    first_screening = forms.ModelChoiceField(queryset=FirstScreening.objects.none(), empty_label=None)
    

    class Meta:
        model = SecondScreening

        fields = ['student_id', 'first_screening', 'acceptance_form','school_fee_receipt','medical_receipt', 
                    'entrepreneur_receipt', 'jamb_admission_letter', 'jamb_original_result', 'attestation_letter', 'status']

        widgets = {
            'student_id': forms.TextInput(attrs={'style': 'display:none'})
        }