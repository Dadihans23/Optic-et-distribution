from django import forms

TYPE_VERRE_CHOICES = [
    ('', '— Sélectionner —'),
    ('UNIFOCAUX', 'UNIFOCAUX'),
    ('PROGRESSIF', 'PROGRESSIF'),
    ('PROGRESSIF FREE-FORM', 'PROGRESSIF FREE-FORM'),
    ('DOUBLE FOYER', 'DOUBLE FOYER'),
    ('POLYCARBONATE', 'POLYCARBONATE'),
    ('MR-8', 'MR-8'),
]

TREATMENT_CHOICES = [
    ('', '— Sélectionner —'),
    ('BLANC', 'BLANC'),
    ('ANTIREFLET SHMC', 'ANTIREFLET SHMC'),
    ('PHOTOCHROMIQUE ANTIREFLET SHMC', 'PHOTOCHROMIQUE ANTIREFLET SHMC'),
    ('PHOTOCHROMIQUE ANTIREFLET SHMC BLUE-CUT UV420', 'PHOTOCHROMIQUE ANTIREFLET SHMC BLUE-CUT UV420'),
]

INPUT_CLASS = 'w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
SELECT_CLASS = 'w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white'


class OrderForm(forms.Form):
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
    # OD
    rightSph = forms.CharField(label='Sph', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0.00'}))
    rightCyl = forms.CharField(label='Cyl', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0.00'}))
    rightAxe = forms.CharField(label='Axe', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0°'}))
    rightAdd = forms.CharField(label='Add', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0.00'}))
    # OG
    leftSph  = forms.CharField(label='Sph', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0.00'}))
    leftCyl  = forms.CharField(label='Cyl', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0.00'}))
    leftAxe  = forms.CharField(label='Axe', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0°'}))
    leftAdd  = forms.CharField(label='Add', max_length=10, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '0.00'}))

    notes = forms.CharField(
        label='Notes',
        required=False,
        widget=forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 3, 'placeholder': 'Informations complémentaires...'}),
    )
