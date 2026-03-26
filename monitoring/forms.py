# from django import forms
# from .models import HealthRecord

# class HealthRecordForm(forms.ModelForm):
#     class Meta:
#         model = HealthRecord
#         fields = ['blood_sugar', 'blood_pressure', 'heart_rate']


from django import forms

class PatientForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    pulse = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    heart_beat = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    blood_pressure = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


class HealthRecordForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField()
    phone_no = forms.CharField(max_length=15)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    pulse = forms.IntegerField()
    heart_rate = forms.IntegerField(label="Heart Beat")
    blood_pressure = forms.CharField(max_length=10)