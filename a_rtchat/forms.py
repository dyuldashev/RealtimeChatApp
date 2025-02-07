from sys import audit

from django.forms import ModelForm
from django import forms
from a_rtchat.models import *

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder':'Add message ...','class': 'p-4 text-black', 'max_length':'300', 'autofocus':True}),
        }

class NewGroupForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name' : forms.TextInput(
                attrs={
                    'placeholder':'Enter group name',
                    'class': 'p-4 text-black',
                    'maxlength':'300',
                    'autofocus':True
                }
            )
        }

class ChatRoomEditForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name' : forms.TextInput(attrs={
                'class': 'p-4 text-xl font-bold mb-4',
                'maxlength':'300',
            })
        }