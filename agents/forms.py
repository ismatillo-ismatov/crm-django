from django import forms
from app.models import Agent
from django.contrib.auth import get_user_model

User = get_user_model()


class AgentModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            "first_name",
            "last_name"
        )

#     def clean_first_name(self):
#         data = self.cleaned_data['first_name']
#
#         return data
#
#     def clean(self):
#         pass
# class AgentForm(forms.Form):
#
#     first_name = forms.CharField()
#     last_name = forms.CharField()
