from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

User = get_user_model()

class UpdatePasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None
    
    class Meta:
        model = User

class UserUpdateForm(forms.ModelForm):
    # forms.IntegerField(widget=forms.HiddenInput(), initial=123) 
    
    # def __init__(self, *args, **kwargs):
    #     self.pk = kwargs.pop('pk')
    #     super().__init__(*args, **kwargs)
        
    #     for fieldname in ['new_password1', 'new_password2']:
    #     self.field['new_password1'].help_text = None

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")