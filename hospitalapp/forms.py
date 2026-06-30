from django import forms
from .models import Patient, Appointment,Prescription


from .models import MedicalRecord
class PatientRegistrationForm(forms.ModelForm):

    username = forms.CharField(max_length=150)

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = Patient
        fields = [
            'name',
            'phone',
            'email',
            'address',
            'username',
            'password',
            'confirm_password'
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password != confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
class MedicalRecordForm(forms.ModelForm):

    class Meta:
        model = MedicalRecord
        fields = '__all__'

class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date']
        widgets = {
            'appointment_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'phone', 'email', 'address']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

class PrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = '__all__'