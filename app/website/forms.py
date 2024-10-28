from django import forms
from .models import Vat_payer_setting

class AddVatPayerSettingsForm(forms.ModelForm):
    class Meta:
        model = Vat_payer_setting
        exclude = ("id",)
        widgets = {
            'druh_reg_DPH': forms.TextInput(attrs={"placeholder": "Druh", "class": "form-control"}),
            'platny': forms.CheckboxInput(attrs={"class": "form-control"}),
        }
        labels = {
            'druh_reg_DPH': "",
            'platny': "",
        }