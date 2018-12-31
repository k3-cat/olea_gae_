
from django import forms


class GForm(forms.Form):
    req = forms.IntegerField()
    staff = forms.TextField()

class TForm(forms.Form):
    req_t = forms.IntegerField()
    staff_t = forms.TextField()
    req_T = forms.IntegerField()
    staff_T = forms.TextField()
