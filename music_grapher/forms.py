from django import forms
from .models import Band

class BandForm(forms.Form):
	band_input = forms.CharField(label='', max_length=50)