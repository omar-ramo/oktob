from django import forms

from .models import User

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given credentials.
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'email_taken': "The email is already taken."
    }
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}), help_text="Enter the same password as before, for verification.")

    class Meta:
        model = User
        fields = ("email", "username" )
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'})
        }

    def clean_email(self):
    	email = self.cleaned_data.get('email')
    	qs = User.objects.filter(email__iexact=email)
    	if(qs.exists()):
    		raise forms.ValidationError(self.error_messages['email_taken'])
    	return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user