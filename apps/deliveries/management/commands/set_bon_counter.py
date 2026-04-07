"""
Initialise ou met à jour le compteur des numéros de bon de livraison.

Usage :
    python manage.py set_bon_counter --month 2026-04 --value 33
    python manage.py set_bon_counter --month 2026-04 --value 33 --settings config.settings.local
"""
from django.core.management.base import BaseCommand
from apps.core.firebase import get_db


class Command(BaseCommand):
    help = 'Initialise le compteur de bons de livraison pour un mois donné'

    def add_arguments(self, parser):
        parser.add_argument('--month', required=True,
                            help='Mois au format YYYY-MM (ex: 2026-04)')
        parser.add_argument('--value', required=True, type=int,
                            help='Dernière valeur utilisée (ex: 33 → prochain sera 04-0034)')

    def handle(self, *args, **options):
        month = options['month']
        value = options['value']

        db = get_db()
        counter_ref = db.collection('counters').document('bon_livraison')
        counter_ref.set({month: value}, merge=True)

        self.stdout.write(self.style.SUCCESS(
            f'✓ Compteur "{month}" défini à {value}. Prochain bon : {month[5:]}-{(value + 1):04d}'
        ))
