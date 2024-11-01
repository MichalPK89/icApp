from django import forms
from django.utils.translation import get_language
from .models import Vat_payer_setting, ItemTranslation

class TranslationsForm(forms.ModelForm):
    class Meta:
        model = ItemTranslation
        exclude = ("id",)
        widgets = {
            'item': forms.TextInput(attrs={"placeholder": "Druh", "class": "form-control", "readonly": "readonly"}),
            'name': forms.TextInput(attrs={"class": "form-control"}),  # Changed from CheckboxInput to TextInput
        }
        labels = {
            'item': "",
            'name': "",
        }

    def __init__(self, *args, **kwargs):
        current_language = get_language()
        super().__init__(*args, **kwargs)

        # Set the item field's initial value and disable it only if item exists
        if hasattr(self.instance, 'item') and self.instance.item:
            self.fields['item'].initial = self.instance.item
            self.fields['item'].disabled = True

        # Filter queryset for name to current language
        self.fields['name'].queryset = ItemTranslation.objects.filter(language_code=current_language)


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