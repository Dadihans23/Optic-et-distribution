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


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Kouamé'}),
        label='Prénom',
    )
    shop_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Optique Lumière'}),
        label='Nom de la boutique',
    )
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

    def clean_first_name(self):
        return self.cleaned_data['first_name'].strip()

    def clean_shop_name(self):
        return self.cleaned_data['shop_name'].strip()
