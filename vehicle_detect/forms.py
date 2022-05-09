from django import forms

from vehicle_detect.models import CommercialParking


class uploadFileForm(forms.Form):
    file = forms.ImageField(label='Whole Car ', label_suffix='')  # for creating file input

class uploadFileSecond(forms.Form):
    file = forms.ImageField(label='Only Plate',label_suffix='')
    file.widget.attrs.update({'class': 'secondModel', 'id': 'secondModel'})

# class signUpForm(forms.Form):
#     # full_name = forms.CharField(initial='Enter Full Name')
#     first_name = forms.CharField(initial='First Name', max_length=20)
#     last_name = forms.CharField(initial='Last Name', max_length=20)
#     username = forms.CharField(initial='Username', max_length=10)
#     email = forms.EmailField(initial='Email', max_length=30)
#     password = forms.CharField(widget=forms.PasswordInput, max_length=10)
#     re_password = forms.CharField(widget=forms.PasswordInput, max_length=10)

# validation
# def clean_password(self):
#     password = self.cleaned_data['password']
#     if len(password) < 4 or len(password) > 6:
#         raise forms.ValidationError("Password is to short")
#     return password

