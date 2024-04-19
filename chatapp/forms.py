from django import forms
from .models import GroupChat


def_atter = { 'class': 'form-control background text-dark' }
check_box_atter = {'class': 'form-check-input'}
class GroupChatUpdateFrom(forms.ModelForm):
    class Meta:
        model =  GroupChat
        exclude = ['manager', 'members', 'created_time', 'address']

        widgets = {
            'name': forms.TextInput(attrs=def_atter),
            'description': forms.Textarea(attrs=def_atter),
            'image': forms.FileInput(attrs=def_atter),
            'can_send_message': forms.CheckboxInput(attrs=check_box_atter),
            'can_see_members': forms.CheckboxInput(attrs=check_box_atter)
        }