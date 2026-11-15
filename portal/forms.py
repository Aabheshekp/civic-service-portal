from django import forms
from .models import ServiceCase

class CaseForm(forms.ModelForm):
    class Meta:
        model = ServiceCase
        fields = ["category", "location", "summary", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 6})}

class StatusForm(forms.Form):
    status = forms.ChoiceField(choices=ServiceCase.Status.choices)
    note = forms.CharField(max_length=500, required=False, widget=forms.TextInput(attrs={"placeholder": "Optional update for the timeline"}))
