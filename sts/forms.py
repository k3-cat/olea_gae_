
from django import forms


class SForm(forms.Form):
    req = forms.IntegerField()
    staff = forms.TextField()
