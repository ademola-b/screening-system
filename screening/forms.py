from django import forms

from accounts.models import CustomUser

from . models import FirstScreening
from . models import SecondScreening

class FirstScreeningUpload(forms.ModelForm):
    # student_id = forms.ModelChoiceField(queryset=Student.objects.none(), empty_label=None)
    class Meta:
        model = FirstScreening

        fields = ['o_level', 'indigene_certificate', 'pry_certificate', 
                    'ND_result', 'admission_letter', 'acceptance_fee_receipt']

        widgets = {
            # 'o_level':forms.FileInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
            'o_level':forms.FileInput(attrs={'class':'form-control', 'id':'formFile'}),
            'indigene_certificate':forms.FileInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
            'pry_certificate':forms.FileInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
            'ND_result':forms.FileInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
            'admission_letter':forms.FileInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
            'acceptance_fee_receipt':forms.FileInput(attrs={'class':'form-control', 'id':'basic-default-name'}),
        }

class SecondScreeningUpload(forms.ModelForm):
    class Meta:
        model = SecondScreening

        fields = ['acceptance_form','school_fee_receipt','medical_receipt', 
                  'entrepreneur_receipt', 'jamb_admission_letter', 'jamb_original_result', 'attestation_letter']

          
        # widgets = {
        #     'student_id': forms.TextInput(attrs={'style': 'display:none'})
        # }

