from django import forms


class PhoneLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: 0102030405',
            'autocomplete': 'tel',
            'inputmode': 'numeric',
        }),
        label='Numéro de téléphone',
    )

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number'].strip().replace(' ', '')
        if not phone.lstrip('+').isdigit():
            raise forms.ValidationError('Numéro de téléphone invalide.')
        return phone
