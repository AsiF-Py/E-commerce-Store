from django import forms
from django.contrib.auth.models import User
from .models import Account,Address
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = Account
        # fields = '__all__'
        fields = ['first_name','last_name','email',]


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs[
                'class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            self.fields[field].widget.attrs[
                'placeholder'] = self.fields[field].label
class LoginFrom(forms.Form):
    email = forms.EmailField(max_length=65,widget=forms.EmailInput)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginFrom, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            self.fields[field].widget.attrs[
                'placeholder'] = self.fields[field].label



from django.contrib.auth.forms import UserChangeForm


class UserProfileUpdateForm(UserChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(), required=False, label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(), required=False, label='Confirm New Password')

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email',]

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if (new_password1 or new_password2) and not old_password:
            raise forms.ValidationError('Please enter your old password to change it.')

        if old_password and not self.instance.check_password(old_password):
            raise forms.ValidationError('Incorrect old password.')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('New passwords do not match.')

        return cleaned_data
    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            self.fields[field].widget.attrs[
                'placeholder'] = self.fields[field].label

class AddressFrom(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
    def __init__(self, *args, **kwargs):
        super(AddressFrom, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
