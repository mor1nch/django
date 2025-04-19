from django import forms

from catalog.models import Product, Version


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['updated_at', 'created_at']

    def __init__(self, *args, **kwargs):
        self.restricted_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                                 'радар']
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data['name']
        for word in self.restricted_words:
            if word in name:
                raise forms.ValidationError(f"Слово {word} запрещено!!")
        return self.cleaned_data['name']

    def clean_description(self):
        description = self.cleaned_data['description']
        for word in self.restricted_words:
            if word in description:
                raise forms.ValidationError(f"Слово {word} запрещено!!")
        return self.cleaned_data['description']


class VersionCreateForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ('version_name', 'version_number', 'current_version')
