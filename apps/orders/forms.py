from django import forms

TYPE_VERRE_CHOICES = [
    ('', '— Sélectionner —'),
    ('DOUBLE FOYER', 'DOUBLE FOYER'),
    ('VISION UNIQUE', 'VISION UNIQUE'),
    ('PROGRESSIF FF', 'PROGRESSIF FF'),
]

TREATMENT_CHOICES = [
    ('', '— Sélectionner —'),
    ('BLANC', 'BLANC'),
    ('ANTIREFLET SHMC', 'ANTIREFLET SHMC'),
    ('PHOTOCHROMIQUE ANTIREFLET SHMC', 'PHOTOCHROMIQUE ANTIREFLET SHMC'),
    ('SOLAIRE', 'SOLAIRE'),
    ('PHOTOCHROMIQUE ANTIREFLET SHMC BLUE-CUT REVÊTEMENT BLEU UV420', 'PHOTOCHROMIQUE ANTIREFLET SHMC BLUE-CUT REVÊTEMENT BLEU UV420'),
    ('PHOTOCHROMIQUE MARRON ANTIREFLET SHMC', 'PHOTOCHROMIQUE MARRON ANTIREFLET SHMC'),
]

INDICE_CHOICES = [
    ('', '— Sélectionner —'),
    ('1.56', '1.56'),
    ('1.59', '1.59'),
    ('1.60', '1.60'),
    ('1.67', '1.67'),
    ('1.74', '1.74'),
]

INPUT_CLASS = 'w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
SELECT_CLASS = 'w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white'


class OrderForm(forms.Form):
    wearerName = forms.CharField(
        label='Nom du porteur',
        max_length=100,
        widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Nom et prénom du porteur'}),
    )
    typeVerre = forms.ChoiceField(
        label='Type de verre',
        required=False,
        choices=TYPE_VERRE_CHOICES,
        widget=forms.Select(attrs={'class': SELECT_CLASS}),
    )
    treatmentOption = forms.ChoiceField(
        label='Traitement',
        required=False,
        choices=TREATMENT_CHOICES,
        widget=forms.Select(attrs={'class': SELECT_CLASS}),
    )
    indice = forms.ChoiceField(
        label='Indice',
        required=False,
        choices=INDICE_CHOICES,
        widget=forms.Select(attrs={'class': SELECT_CLASS}),
    )
    nombrePaires = forms.IntegerField(
        label='Nombre de paires',
        required=False,
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': INPUT_CLASS, 'min': 1, 'placeholder': '2 paires'}),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Commandes historiques saisies en texte libre : on conserve leur valeur
        # actuelle comme option (édition) pour ne pas la perdre silencieusement.
        for name in ('typeVerre', 'treatmentOption', 'indice'):
            current = self.initial.get(name)
            field = self.fields[name]
            if current and current not in {v for v, _ in field.choices}:
                field.choices = list(field.choices) + [(current, current)]

    def clean_nombrePaires(self):
        return self.cleaned_data.get('nombrePaires') or 1
