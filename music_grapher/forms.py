from django import forms
from .models import Band

class BandForm(forms.Form):
	band_input = forms.CharField(label='', max_length=50)
	json_string = forms.CharField(widget=forms.HiddenInput(), required=False)