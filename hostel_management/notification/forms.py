from django import forms

class SMSSendForm(forms.Form):
    phone_number = forms.CharField(max_length=15)
    message = forms.CharField(widget=forms.Textarea)
