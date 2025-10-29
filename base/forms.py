from django.forms import ModelForm 
from django import forms
from .models import Room
from .models import Message
from .models import User



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  
        exclude = ['participants', 'host']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']  # only the field the user can edit
        widgets = {
            # Change TextField to a single-line <input type="text">
            'body': forms.TextInput(attrs={'placeholder': 'Write a comment…'}),
            }
        


class UserForm(ModelForm):
    # Add about field manually (not linked to User model)
    about = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Write about yourself...'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']  # Model fields only