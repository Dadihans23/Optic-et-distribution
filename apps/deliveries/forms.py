from django import forms
from apps.orders.forms import INPUT_CLASS, TYPE_VERRE_CHOICES, TREATMENT_CHOICES


class DeliveryRequestForm(forms.Form):
    wearerName = forms.CharField(
        label='Nom du porteur',
        max_length=100,
        widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Nom et prénom du porteur'}),
    )
    typeVerre = forms.CharField(
        label='Type de verre',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Saisir ou choisir dans la liste',
            'list': 'typeVerreList',
        }),
    )
    treatmentOption = forms.CharField(
        label='Traitement',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Saisir ou choisir dans la liste',
            'list': 'treatmentList',
        }),
    )
    rightSph = forms.CharField(label='Sph', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0.00'}))
    rightCyl = forms.CharField(label='Cyl', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0.00'}))
    rightAxe = forms.CharField(label='Axe', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0°'}))
    rightAdd = forms.CharField(label='Add', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0.00'}))
    leftSph  = forms.CharField(label='Sph', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0.00'}))
    leftCyl  = forms.CharField(label='Cyl', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0.00'}))
    leftAxe  = forms.CharField(label='Axe', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0°'}))
    leftAdd  = forms.CharField(label='Add', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0.00'}))
    notes = forms.CharField(
        label='Notes',
        required=False,
        widget=forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 3, 'placeholder': 'Informations complémentaires...'}),
    )
